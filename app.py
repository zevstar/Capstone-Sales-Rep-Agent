import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults


# Model and Agent tools
llm = ChatGroq(api_key=st.secrets.get("GROQ_API_KEY"))
search = TavilySearchResults(max_results=2)
parser = StrOutputParser()
# tools = [search] # add tools to the list

# Page Header
st.title("Assistant Agent")
st.markdown("Assistant Agent Powered by Groq.")


# Data collection/inputs
with st.form("company_info", clear_on_submit=True):

    product_name = st.text_input("**Product Name** (What product are you selling?):")
    
    company_url = st.text_input(
        "**Company URL** (The URL of the company you are targeting):"
    )
    
    product_category = st.text_input(
        "**Product Category** (e.g., 'Data Warehousing' or 'Cloud Data Platform')"
    )
    
    competitors_url = st.text_input("**Competitors URL** (ex. www.apple.com):")
    
    value_proposition = st.text_input(
        "**Value Proposition** (A sentence summarizing the product’s value):"
    )
    
    target_customer = st.text_input(
        "**Target Customer** (Name of the person you are trying to sell to.) :"
    )

    # For the llm insights result
    company_insights = ""

    # Data process
    if st.form_submit_button("Generate Insights"):
        if product_name and company_url:
            st.spinner("Processing...")

            # Use search tool to get Company Information
            company_information = search.invoke(company_url)
            print(company_information)

            # TODO: Create prompt <=================
            prompt = """ You are a sales and marketing assistant. Analyze the following information:

      Product Name: {product_name}
      Company details: {company_information}
      Competitor URL: {competitors_url}

      Your goal is to help sales representatives gain insights into prospective accounts, competitors, and company strategy.

      For the Product Name and each competitor produce a one page summary with the following sections:
      
      1. Provide a brief narrative of the company strategy including insights into the company's activities and priorities.
      
      2. List mentions of competitors for input URLs or scraped data.
      
      3. List leadership information including names, titles, and email addresses.
      
      4. Provide a product strategy and summary inclduing insights form public documents and reports. Highlight special features in each product. 
      
      5. Provide links to articles, press releases, and other sources.
      
      6. Analyze the following company information and summarize its strategy, key leadership, and mentions of competitors. Look for mentions of comepetitors in review sites.
      

      Provide the results in a table with shading alternating rows.


      
      In addition, provide links to all of the websites where data was obtained.

      
      
      """

            # Prompt Template
            prompt_template = ChatPromptTemplate([("system", prompt)])

            # Chain
            chain = prompt_template | llm | parser

            # Result/Insights
            company_insights = chain.invoke(
                {
                    "company_information": company_information,
                    "target_customer": target_customer,
                    "product_name": product_name,
                    "competitors_url": competitors_url,
                    "product_category": product_category,
                    "value_proposition": value_proposition
                    
                }
            )

st.markdown(company_insights)
