# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.
import json
from odoo import api, fields, models, tools
from odoo.exceptions import UserError, ValidationError

import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough


class WhatsappHistory(models.Model):
    _inherit = "whatsapp.history"

    def process_rag_chain(self, input_data, persist_directory):
        # Initialize the Chroma vector store
        if self.env.company.open_ai_api_key:
            os.environ["OPENAI_API_KEY"] = self.env.company.open_ai_api_key
        else:
            raise UserError("No OpenAI API key found.")

        db3 = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())
        docs = db3.similarity_search(input_data)
        # Define the prompt template
        template = """
           Use the following pieces of context to provide a detailed answer to the question at the end.
           Act as a traveler agent. Your role is to give guidance on it.
           If user input is a greeting, you should greet.
           {context}
           Question: {question}
           Helpful Answer:
           """
        # Initialize the ChatOpenAI model

        if self.env.company.open_ai_model and self.env.company.open_ai_max_tokens:
            llm = ChatOpenAI(model=self.env.company.open_ai_model, max_tokens=self.env.company.open_ai_max_tokens)
        else:
            raise UserError("No OpenAI model found.")

        # Create a retriever from the Chroma vector store
        retriever = db3.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        # Create the custom prompt template
        custom_rag_prompt = PromptTemplate.from_template(template)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # Create the RAG chain
        rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | custom_rag_prompt
                | llm
                | StrOutputParser()
        )
        # Invoke the chain with the user input
        result = rag_chain.invoke(input_data)
        return result

    def get_response(self, input_data):
        persist_directory = 'chroma'
        return self.process_rag_chain(input_data, persist_directory)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            provider_id = self.env["provider"].browse(int(vals.get("provider_id", False)))
            partner_id = self.env["res.partner"].browse(int(vals.get("partner_id", False)))
            user = provider_id.user_id
            channel = provider_id.get_channel_whatsapp(partner_id, user)
            chatbot = self.env['whatsapp.chatbot'].browse(int(self._get_active_chatbot()))
            if vals.get("message") and vals.get("type") == "received":
                if chatbot and chatbot.mapped("step_type_ids").filtered(
                            lambda l: l.step_call_type == 'pdf'):
                    # Bot
                    if not channel.is_chatbot_ended:
                        message_script = chatbot.mapped("step_type_ids").filtered(
                            lambda l: l.message == vals.get("message"))
                        current__chat_seq_script = chatbot.mapped("step_type_ids").filtered(
                            lambda l: l.sequence == channel.script_sequence)
                        if message_script:
                            chatbot_script_lines = message_script
                        elif current__chat_seq_script and not current__chat_seq_script.step_call_type == "action":
                            chatbot_script_lines = current__chat_seq_script
                        else:
                            chatbot_script_lines = provider_id.company_id.wa_chatbot_id.step_type_ids[0]

                        for chat in chatbot_script_lines:
                            if chat.sequence >= channel.script_sequence:
                                channel.write(
                                    {
                                        "wa_chatbot_id": chat.whatsapp_chatbot_id.id if provider_id.company_id and provider_id.company_id.wa_chatbot_id == chat.whatsapp_chatbot_id else
                                        False,
                                        "script_sequence": chat.sequence,
                                    }
                                )
                            elif (
                                    current__chat_seq_script
                                    and current__chat_seq_script.parent_id
                                    and current__chat_seq_script.parent_id
                                    == chat.parent_id
                            ):
                                channel.write(
                                    {
                                        "wa_chatbot_id": chat.whatsapp_chatbot_id.id,
                                        "script_sequence": chat.sequence,
                                    }
                                )
                            else:
                                first_script = chatbot.mapped("step_type_ids").filtered(lambda l: l.sequence == 1)
                                if first_script:
                                    channel.write(
                                        {
                                            "wa_chatbot_id": chat.whatsapp_chatbot_id.id,
                                            "script_sequence": first_script.sequence,
                                        }
                                    )
                                else:
                                    channel.write(
                                        {
                                            "wa_chatbot_id": chat.whatsapp_chatbot_id.id if provider_id.company_id and provider_id.company_id.wa_chatbot_id == chat.whatsapp_chatbot_id
                                            else False,
                                            "script_sequence": chat.sequence,
                                        })

                            message_values = {
                                "author_id": user.partner_id.id,
                                "email_from": user.partner_id.email or "",
                                "model": "discuss.channel",
                                "message_type": "wa_msgs",
                                "wa_message_id": vals.get("message_id"),
                                "isWaMsgs": True,
                                "subtype_id": self.env["ir.model.data"]
                                .sudo()
                                ._xmlid_to_res_id("mail.mt_comment"),
                                "partner_ids": [(4, partner_id.id)],
                                "res_id": channel.id,
                                "reply_to": partner_id.email,
                                "company_id": vals.get("company_id"),
                                "wa_chatbot_id": chat.whatsapp_chatbot_id.id,
                            }

                            if chat.step_call_type == "pdf":
                                if chat.chatbot_document_ids:
                                    chat_answer = self.get_response(vals.get('message'))
                            message_values.update({'body': chat_answer})
                            self._send_wa_message(provider_id, channel, message_values)
                else:
                    return super().create(vals)
            return super().create(vals)