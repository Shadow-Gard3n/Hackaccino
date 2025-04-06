from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from os import getenv
load_dotenv()
#from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, END, StateGraph, MessagesState
from typing import Annotated, TypedDict
from operator import add
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

sqlite_conn = sqlite3.connect("checkpoint.sqlite1", check_same_thread=False)
memory = SqliteSaver(sqlite_conn)
from langchain_openai import ChatOpenAI
#from langchain_deepseek import ChatDeepSeek
import asyncio
#from crawl4ai import *
from langchain_linkup import LinkupSearchTool
import streamlit as st
from langchain_ollama import ChatOllama
import ast

class state_content(TypedDict):
    query: Annotated[list[str], add]
    llm_user_query_content: list[str]
    llm_user_query_further1_content: list[str]
    llm_user_query_further2_content: list[str]
    llm_user_query_further3_content: list[str]
    link_web_search: list[str]
    llm_merge_content: Annotated[list[str], add]
    llm_summary_content: str


graph = StateGraph(state_content)


def web_search(State: state_content):
    query = State["llm_user_query_further1_content"] + State["llm_user_query_further2_content"] + State[
        "llm_user_query_further3_content"]
    print(query)
    api_key = getenv("LINKUP_API_KEY")
    tool = LinkupSearchTool(
        depth="standard",  # "standard" or "deep"
        output_type="searchResults",  # "searchResults", "sourcedAnswer" or "structured"
        linkup_api_key=api_key, )
    scraped_link = []
    k=0
    for j in query:
        ques = ("THIS IS THE QUESTION " + str(k + 1) + " <QUESTION_" + str(k + 1) + ">" + str(j) + "</QUESTION_" + str(
            k + 1) + ">")
        scraped_link.append(ques)
        result = tool.invoke({"query": j})
        for i in range(len(result.results)):
            st.write(result)
            t=result.results[i].content
            ans = (f"THIS IS THE ANSWER {str(i + 1)} of QUESTION {str(k + 1)} <ANSWER_{str(i + 1)}>{t}</ANSWER_{str(i + 1)}>")
            #ans = ("THIS IS THE ANSWER " + str(i + 1) + " of QUESTION " + str(k + 1) + "<ANSWER_" + str(i + 1) + ">" + (result.results[i].content) + "</ANSWER_" + str(i + 1) + ">")
            scraped_link.append(ans)
            k=k+1

    return {"link_web_search": scraped_link}

def pro_search_call(topic,thread_number):
    # it is used for getting user query and return content for tool search of 3 seperate content
    try:
        llm_user_query_openai = ChatOpenAI(model="gpt-4o-mini", temperature=1)
    except Exception as e:
        print(e)

    openai_user_query_prompt = [('system', """A conversation between User and Assistant. The user asks a question, and the Assistant solves it. The assistant first thinks about the reasoning process in the mind and then provides the user with the answer. The reasoning process and answer are enclosed within <think> </think> and <answer> </answer> tags, respectively, i.e., <think> reasoning process here </think>
    <answer> answer here </answer>."""),
                                ('human', """Create three well-structured and diverse queries that explore different dimensions of the user query by following a step-by-step approach to answer the question. So that each query targets a unique aspect of the query and can be used for effective web searches. You are provided with a template for your answer. CAPITALISED words are the placeholders. Fill in the placeholders with your answer. NOTE- Make sure to preserve the overall formatting of the template also each answer should contain @ at the start and end of each search query.


    <think> </think>
    <answer>
    @QUERY1@QUERY2@QUERY3@
    </answer>

    The user query is{QUERY_USER}""")]

    openai_user_query_template = ChatPromptTemplate.from_messages(openai_user_query_prompt)

    openai_user_query_call = openai_user_query_template | llm_user_query_openai | StrOutputParser()


    def user_query_execute(State: state_content):
        result = openai_user_query_call.invoke({"QUERY_USER": State["query"][-1]}).split("@")

        return {"llm_user_query_content": result[1:4]}


    def user_query_further1_execute(State: state_content):
        result = openai_user_query_call.invoke({"QUERY_USER": State["llm_user_query_content"][0]}).split("@")

        return {"llm_user_query_further1_content": result[1:4]}


    def user_query_further2_execute(State: state_content):
        result = openai_user_query_call.invoke({"QUERY_USER": State["llm_user_query_content"][1]}).split("@")

        return {"llm_user_query_further2_content": result[1:4]}


    def user_query_further3_execute(State: state_content):
        result = openai_user_query_call.invoke({"QUERY_USER": State["llm_user_query_content"][2]}).split("@")

        return {"llm_user_query_further3_content": result[1:4]}


    # it is used to getting all link content and give output of merge it
    try:
        llm_merge_openai = ChatOpenAI(model="gpt-4o-mini", max_completion_tokens=2000, temperature=0.3)
    except Exception as e:
        print(e)

    openai_merge_prompt = [("system",
                            """You are an expert in understanding unstructured data, identifying relationships within the data, and creating comprehensive content. You also excel at finding relevant information that covers different aspects of the any query.
                            """),
                        ("human", """Your task is to answer user query solely based on the two content that is provided to you. Ensure no additional information or knowledge is included from your tranning data that is realted to the query. Maintain accuracy and relevance while structuring your response clearly. The first content is going to be 9 question each followed by 10 answer that may or may not be related to query. the second content is the summary of past output they where generated by you to answer user query. Use this summarised history only when you think it is going to be relevent to answer user query or user has asked a quetion related to your past output.

    The format of the first content is that there will be 9 question each followed by 10 answer.

    this is the first - {m2}
    this is the second {m1}
    The word count of the output should be from 250 to 500 words.
    """)]

    openai_merge_template = ChatPromptTemplate.from_messages(openai_merge_prompt)

    openai_merge_call = openai_merge_template | llm_merge_openai | StrOutputParser()


    def merge_execute(State: state_content):
        if State.get("llm_summary_content"):
            return {"llm_merge_content": [
                openai_merge_call.invoke({"m1": State["llm_summary_content"], "m2": State["link_web_search"]})]}
        else:
            return {"llm_merge_content": [openai_merge_call.invoke({"m1": "", "m2": State["link_web_search"]})]}


    # it is used to getting merge content and give summary content

    try:
        llm_summary_openai = ChatOpenAI(model="gpt-4o-mini")
    except Exception as e:
        print(e)

    openai_summary_prompt = [('system',
                            """You will be provided with two content. Your task is to:
                            1.⁠ ⁠Condense the content by removing filler words, redundant phrases, and non-essential linguistic elements (e.g., repetitive verbs, adverbs, or vague descriptors) while retaining all factual details, definitions, subsections, and contextual examples.
                            2.⁠ ⁠Structure the information into clear, hierarchical bullet points:
                                - Group related ideas under subheadings that mirror the original content’s organization.
                                - Preserve lists, definitions, and relationships between concepts
                                - Include all subsections even if briefly mentioned.
                            3. ⁠Ensure completeness:
                                - Do not omit any named sections, tools, methods, or applications.
                                - Retain quoted definitions and specific examples from the original text.
                            4.⁠ ⁠Prioritise accuracy and clarity over brevity. """
                            ), ('human',
                                "HERE THIS IS THE FRIST CONTENT -  <CONTENT_1>{summary}</CONTENT_1>. HERE THIS IS THE SECOND CONTENT <CONTENT_2>{merge}</CONTENT_2>"
                                )]

    openai_summary_template = ChatPromptTemplate.from_messages(openai_summary_prompt)

    openai_summary_call = openai_summary_template | llm_summary_openai | StrOutputParser()


    def summary_execute(State: state_content):
        if State.get("llm_summary_content"):
            return {"llm_summary_content": openai_summary_call.invoke(
                {"summary": State["llm_summary_content"], "merge": State["llm_merge_content"][-1]})}
        else:
            return {
                "llm_summary_content": openai_summary_call.invoke({"summary": "", "merge": State["llm_merge_content"][-1]})}


    graph.add_node("LLM_USER_QUERY_DISPLAY", user_query_execute)
    graph.add_node("LLM_USER_QUERY_FURTHER1_DISPLAY", user_query_further1_execute)
    graph.add_node("LLM_USER_QUERY_FURTHER2_DISPLAY", user_query_further2_execute)
    graph.add_node("LLM_USER_QUERY_FURTHER3_DISPLAY", user_query_further3_execute)
    graph.add_node("LINK_EXTARACT", web_search)
    graph.add_node("LLM_MERGE_DISPLAY", merge_execute)
    graph.add_node("LLM_SUMMARY_DISPLAY", summary_execute)

    graph.add_edge(START, "LLM_USER_QUERY_DISPLAY")
    graph.add_edge("LLM_USER_QUERY_DISPLAY", "LLM_USER_QUERY_FURTHER1_DISPLAY")
    graph.add_edge("LLM_USER_QUERY_DISPLAY", "LLM_USER_QUERY_FURTHER2_DISPLAY")
    graph.add_edge("LLM_USER_QUERY_DISPLAY", "LLM_USER_QUERY_FURTHER3_DISPLAY")
    graph.add_edge("LLM_USER_QUERY_FURTHER1_DISPLAY", "LINK_EXTARACT")
    graph.add_edge("LLM_USER_QUERY_FURTHER2_DISPLAY", "LINK_EXTARACT")
    graph.add_edge("LLM_USER_QUERY_FURTHER3_DISPLAY", "LINK_EXTARACT")
    graph.add_edge("LINK_EXTARACT", "LLM_MERGE_DISPLAY")
    graph.add_edge("LLM_MERGE_DISPLAY", "LLM_SUMMARY_DISPLAY")
    graph.add_edge("LLM_SUMMARY_DISPLAY", END)

    app = graph.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": thread_number}}
    result = app.invoke({"query": [topic]}, config=config)

    x = app.get_state(config).values
    dictx = dict()
    dictx["query"] = x["query"]
    dictx["llm_merge_content"] = x["llm_merge_content"]

    file = open("pro_search.txt"+str(thread_number), "w")
    file.write(str(dictx))
    file.flush()
    return dictx

def pro_search_txt(thread_number):
    file = open("pro_search.txt"+str(thread_number), "r")
    f=file.read()
    a=ast.literal_eval(f)
    return (a)