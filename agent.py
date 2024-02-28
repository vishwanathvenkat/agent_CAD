from autogen import UserProxyAgent, config_list_from_json, AssistantAgent, agentchat
from model import create_point
from typing_extensions import Annotated
import irit


def main():
    # Load LLM inference endpoints from an env variable or a file
    # See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
    # and OAI_CONFIG_LIST_sample.
    # For example, if you have created a OAI_CONFIG_LIST file in the current working directory, that file will be used.
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

    # Create the agent that uses the LLM.
    assistant = AssistantAgent("assistant",
                               llm_config={"config_list": config_list, "temperature": 0},
                               system_message="""
                                              You create a random 3D point and plot them on users' request.   
                                              YOu categorize the points as X, Y, Z coordinate and pass it back to the user for approval. 
                                              The points are in the range (-10, 10). They can be float values
                                              Once approved you call the plotter function to plot the point.                                                                                           
                                              Reply "TERMINATE" in the end when everything is done.                                                                                        
                                              """
                               )

    # Create the agent that represents the user in the conversation.
    user_proxy = UserProxyAgent(
        name="user_proxy",
        # is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        max_consecutive_auto_reply=10,
        human_input_mode='ALWAYS',
        code_execution_config={
            "use_docker": False
        }
    )

    @user_proxy.register_for_execution()
    @assistant.register_for_llm(description="plot the points")
    def point_plotter(
            x: Annotated[float, "x coordinate of the point"],
            y: Annotated[float, "y coordinate of the point"],
            z: Annotated[float, "z coordinate of the point"]
    ):
        ctlpt = irit.ctlpt(irit.E3, x, y, z)
        irit.interact(ctlpt)
        return f"Point displayed"

    user_proxy.initiate_chat(assistant, message="Create a point for me ")


if __name__ == "__main__":
    main()
