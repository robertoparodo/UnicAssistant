"""
The "LLM" script handles the chatbot's logic.
Within this class, several essential tasks are performed.
First, it loads the vector database containing all the necessary information to respond to user queries.
Secondly, it uses LangChain to create the process for retrieving the most relevant information and generating responses.
Other tools used include query decomposition, if needed, and conversation history management.

Author:
Roberto Parodo, email: r.parodo2@studenti.unica.it
"""
from langchain_openai import AzureChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.retrievers.multi_query import MultiQueryRetriever
from load_db import VectorizedDb

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="config.env")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class Llm(object):
    def __init__(self, course):
        """
        This class enables querying the database and generating responses.
        Before starting the Bot, make sure to set up the API keys.

        :param course: It is necessary to correctly identify the degree program being referred to and is used to
        accurately locate the segments from which to extract the information.
        """
        self.course = course
        #self.llm = AzureChatOpenAI(
        #    openai_api_key=os.getenv("OPENAI_API_KEY"),
        #    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        #    api_version=os.getenv("OPENAI_API_VERSION"),
        #    deployment_name=os.getenv("DEPLOYMENT_NAME")
        #)
        self.llm = ChatOpenAI(
           model="gpt-3.5-turbo"
        )
        self.database = VectorizedDb().get_db()
        self.chain = self.create_chain(self.database)
        self.chat_history = []
    
    def create_chain(self, vectorstore):
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "Sei un chatbot che aiuta gli studenti a capire i regolamenti devi rispondere brevemente in base a questi documenti rilevanti: "
             "{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=prompt
        )
        retriever = MultiQueryRetriever.from_llm(
            retriever=vectorstore.as_retriever(search_kwargs={"filter": {"source": self.course}, "k": 5}), llm=self.llm
        )
        retrieval_chain = create_retrieval_chain(
            retriever,
            chain
        )
        return retrieval_chain

    def process_chat(self, question):
        if not self.composite_query(question):
            response = self.chain.invoke({
                "chat_history": self.chat_history,
                "input": question,
            })
            self.chat_history.append(HumanMessage(content=question))
            self.chat_history.append(AIMessage(content=response["answer"]))
            return response
        else:
            print("è una query composta")
            subquery = self.decomposite_query(question)
            if not subquery:
                return self.process_chat_sub_query(question)
            else:
                response_composed = []
                for query in subquery:
                    response_composed.append(self.process_chat_sub_query(query)["answer"])
                return {"answer": "\n".join(response_composed)}

    def process_chat_sub_query(self, question):
        response = self.chain.invoke({
            "chat_history": self.chat_history,
            "input": question,
        })
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=response["answer"]))
        return response

    def composite_query(self, question):
        messages = [
            AIMessage(content="Determina se la seguente query è composta da più domande o semplice\n Devi rispondere solamente con composta o semplice:"),
            HumanMessage(content=question),
        ]
        response = self.llm.invoke(messages)
        return "composta" in response.content

    def decomposite_query(self, question):
        messages = [
            AIMessage(content="Decomponi la seguente domanda nelle sotto-domande che sono esplicitamente presenti, senza aggiungerne altre o inventarne di nuove"),
            HumanMessage(content=question),
        ]
        response = self.llm.invoke(messages)
        print(response)
        sub_query = [element for element in response.content.split("\n") if element.strip().startswith(('1', '2'))]
        print(sub_query)
        return sub_query
