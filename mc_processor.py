import pandas as pd
import visualizing
import os

def clean_key(key_name):
    try:
        if '---' in key_name:
            return key_name.split(' --- ')[1].strip()
        # elif \\ in keyname
        elif '\\\\' in key_name:
            return key_name.split('\\\\')[1].strip()
        else:
            return key_name
    except:
        return key_name
    
def get_name_from_codebook(codebook, question, level):
    return codebook.loc[(codebook["question"] == question) & (codebook["value"] == level), "code"].values[0]
    
def get_percent_select_multiple_base(data,q_codebook,question="BPC1") -> dict:
    """
    Returns the percentage of respondents who selected each option for a given question. 
    """
    weighted_numerator = {}
    weighted_denominator = {}

    # select all columns including question text
    for question_option in data.filter(regex='^'+question+"_").columns:
        # calculate weighted numerator and denominator (aka # of respondents who selected each option)
        weighted_numerator[question_option] = ((data[question_option] == 1) * data['wts']).sum()
        weighted_denominator[question_option] = ((data[question_option] == 1) * data['wts']).sum() + \
                                                ((data[question_option] == 2) * data['wts']).sum()

    # divide numerator by denominator
    weighted = {}
    for key in weighted_numerator.keys():
        if "TEXT" not in key:
            weighted[key] = weighted_numerator[key] / weighted_denominator[key]

    # replace weighted key name with value from 
    weighted = {q_codebook[key]: value for key, value in weighted.items()}

    # clean (remove question text from response category)
    weighted = {clean_key(k): v for k, v in weighted.items()}

    return weighted


def get_percents_select_one_base(data,codebook,question):
    """
    Returns percent of respondents who selected each option for 'select one' questions
    """
    numerators = data.groupby(question).apply(lambda x: x['wts'].sum())
    denominator = numerators.sum()

    results = numerators/denominator

    new_index = []
    for index in results.index:
        new_index.append(get_name_from_codebook(codebook,question,index))

    results.index = new_index
        
    return results

def data_type_check(data,q_columns):
    """
    returns boolean value indicating question type
    """
    matrix = False
    multiple_selections = False

    if len(q_columns) == 0: # underscore only used when each option has selections
        return multiple_selections, matrix # single selection

    ## to address single select questions with a short response text answer
    elif (len(q_columns) == 1) and ("TEXT" in q_columns[0]):
        return multiple_selections, matrix # single selection

    ## selects matrix quetsion (if BOTH multiple columns per question and multiple response categories within each column)
    elif (len(q_columns) > 1) and (len(data[[q_columns[0]]].dropna()[q_columns[0]].unique()) > 2):
        matrix = True
        return multiple_selections, matrix

    ## otherwise, probably mulitple selections
    else:
        multiple_selections = True
        return multiple_selections, matrix

def get_percents(data,codebook,q_codebook,question="BPC1",demo=None):
    """
    Returns percent who selected each option,
    works for questions that have multiple or single selection.

    Demo input optional.
    """
    #boolean check for question type
    
    q_columns = data.filter(regex='^'+question+"_").columns
    multiple_selections, matrix = data_type_check(data,q_columns)

    try:
        # if all na
        if data[question].isnull().all():
            print(f"{question}: all NA values")
            # return
    except:
        pass

    #holder dict
    demo_results = {}

    #if demo provided
    if demo:
        for demo_group, group_data in data.groupby([demo]):
            #lookup demo name
            demo_category_name = get_name_from_codebook(codebook,demo,demo_group[0])
            
            #store to results dict
            if multiple_selections:
                demo_results[demo_category_name] = get_percent_select_multiple_base(group_data,q_codebook,question)
            
            elif matrix:
                #create multi-level index
                demo_results[demo_category_name] = {}

                # for each matrix level
                for q in q_columns:
                    demo_results[demo_category_name][clean_key(q_codebook[q])] = get_percents_select_one_base(group_data,codebook,q)
                    
            else:
                demo_results[demo_category_name] = get_percents_select_one_base(group_data,codebook,question)

    #either way, add results for overall pop
    if multiple_selections:
        demo_results["overall"] = get_percent_select_multiple_base(data,q_codebook,question)

    elif matrix:
        for q in q_columns:
            if demo:
                demo_results[demo_category_name][clean_key(q_codebook[q])] = get_percents_select_one_base(data,codebook,q)

            else:
                demo_results[clean_key(q_codebook[q])] = get_percents_select_one_base(data,codebook,q)

    else:
        demo_results["overall"] = get_percents_select_one_base(data,codebook,question)

    #return pandas df
    if matrix: #format as multilevel index

        if demo:
            flattened_dict = {
                (dem_group, question): results
                for dem_group, questions in demo_results.items()
                for question, results in questions.items()
            }

            df = pd.DataFrame.from_dict(flattened_dict, orient='index').T
            
            return df #.sort_values(by=df.columns[0])

        #if matrix but not demo
        else:
            return pd.DataFrame(demo_results).T
        
    else:
        return pd.DataFrame(demo_results) #.sort_values(by='overall')
    
def get_question_text(q_codebook, question):
    question_text = q_codebook[[i for i in q_codebook if i.startswith(question)][0]]
    if '---' in question_text:
        question_text = question_text.split('---')[0]
    elif '\\\\' in question_text:
        question_text = question_text.split('\\\\')[0]
    return question_text

def get_parallel_questions(data, codebook, q_codebook, questions, demo=None):
    dfs = []
    for question in questions:
        question_text = get_question_text(q_codebook, question)
        df = run_and_display(data,codebook,q_codebook,question,demo,suppress_output=True)
        display(df)
        df.columns = [question_text]
        dfs.append(df)

    df = pd.concat(dfs, axis=1)
    
    return df


def run_and_display(data,codebook,q_codebook,question,demo=None,suppress_output=False,sort=True,save_fig_path = None):
    """
    Runs and displays results for a given question
    """

    try:
        results = get_percents(data,codebook,q_codebook,question,demo)
        if sort:
            results = results.sort_values(by=results.columns[0])

        if not os.path.exists(f"processed/"):
            os.makedirs(f"processed/")
        
        if demo:
            # create demo directory
            if not os.path.exists(f"processed/{demo}"):
                os.makedirs(f"processed/{demo}")
            # save to demo directory
            results.to_csv(f"processed/{demo}/{question}.csv")
        else:
            results.to_csv(f"processed/{question}.csv")

        if not suppress_output:
            question_text = get_question_text(q_codebook, question)
            visualizing.plot_question(results, question, question_text, sort=sort,save_fig_path = save_fig_path)

        return results

    except Exception as e:
        print(f"*Issue with {question}: {str(e)[:300]}\n")


### IGNORE SPLIT SAMPLE

def get_confidence_results(data, codebook, q_codebook, question='BPC20', demo=None, suppress_output=False):
    question_a = f"{question}a"
    if not suppress_output:
        print(f"{question}: {q_codebook[question_a]}")

    demo_results = {}

    if demo:
        for demo_group, group_data in data.groupby([demo]):
            demo_category_name = get_name_from_codebook(codebook, demo, demo_group)
            numerators = group_data.groupby(question).apply(lambda x: x['wts'].sum())
            denominator = numerators.sum()
            results = numerators / denominator
            new_index = [get_name_from_codebook(codebook, question_a, index) for index in results.index]
            results.index = new_index
            demo_results[demo_category_name] = results

    numerators = data.groupby(question).apply(lambda x: x['wts'].sum())
    denominator = numerators.sum()
    results = numerators / denominator
    new_index = [get_name_from_codebook(codebook, question_a, index) for index in results.index]
    results.index = new_index
    demo_results["overall"] = results

    return pd.DataFrame(demo_results).sort_values(by='overall', ascending=False)