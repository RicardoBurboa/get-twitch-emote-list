"""
    Script to fetch the channel's emote list from a user list from Twitch. Then export that in a CSV in the directory the script is located.

    Using the twitchAPI package for Python.
    Install with "pip install twitchAPI".
"""



def Get_User_ID_And_Name_From_List(Twitch_Client_ID: str, Twitch_Secret: str, User_List: list) -> list:
    """
    Parameters
    ----------

    Twitch_Client_ID: str
        Twitch client ID token variable.
    Twitch_Secret: str
        Twitch secret token variable.
    User_List: list
        List of users that the person that is running the script wants to know about. Only need to create a list with the channel names displayed on Twitch.
        Example: User_List = ["Channel1", "Channel2", "Channel3"]

    Returns
    -------

    User_List: list
        List of users containing the User ID and the Username displayed on Twitch.
        Order of items: [User_ID, User_Name]
    """
    
    # List that will contain the lists of all the channels' information.
    User_Matrix = []

    # Twitch object that handles the requests. Needs Twitch credentials.
    from twitchAPI.twitch import Twitch
    Twitch_Object = Twitch(Twitch_Client_ID, Twitch_Secret)
    
    # Fetch the information from the user list that was provided.
    User_Info = Twitch_Object.get_users(logins = User_List)

    # User_Info is a dictionary, and we only need the Data from it.
    User_Data = User_Info["data"]

    # Loop through the user list that was provided.
    User_Data_Size = len(User_Data)
    for User_Iterator in range(User_Data_Size):
        
        User_Data_Dict = User_Data[User_Iterator]
        User_ID = User_Data_Dict["id"]
        User_Name = User_Data_Dict["display_name"]

        User_Matrix_Row = []
        User_Matrix_Row.append(User_ID)
        User_Matrix_Row.append(User_Name)
        User_Matrix.append(User_Matrix_Row)

    return User_Matrix


def Get_Emote_List(Twitch_Client_ID: str, Twitch_Secret: str, User_List: list) -> list:
    """
    Parameters
    ----------

    Twitch_Client_ID: str
        Twitch client ID token variable.
    Twitch_Secret: str
        Twitch secret token variable.
    User_List: list
        List of users containing the User ID and the Username displayed on Twitch.
        Order of items: [User_ID, User_Name]

    Returns
    -------
    Emote_List_Matrix: list
        List of emotes the channel has.
        Order of items: [Channel, Emote_Name, Emote_List]
    """
    
    # Emote matrix.
    Emote_List_Matrix = []

    # Twitch object that handles the requests. Needs Twitch credentials.
    from twitchAPI.twitch import Twitch
    Twitch_Object = Twitch(Twitch_Client_ID, Twitch_Secret)

    # Loop through each user.
    User_Data_Size = len(User_List)

    for User_Iterator in range(User_Data_Size):
        User_ID = User_List[User_Iterator][0]
        User_Name = User_List[User_Iterator][1]

        Emote_Info = Twitch_Object.get_channel_emotes(User_ID)

        Emote_Data = Emote_Info["data"]
        Emote_Info_Size = len(Emote_Data)

        for Emote_Iterator in range(Emote_Info_Size):
            Emote_Row = []
            Emote_Data_Dict = Emote_Data[Emote_Iterator]
            
            Emote_Name = Emote_Data_Dict["name"]
            Emote_URL = Emote_Data_Dict["images"]["url_4x"]

            Emote_Row.append(User_Name)
            Emote_Row.append(Emote_Name)
            Emote_Row.append(Emote_URL)

            Emote_List_Matrix.append(Emote_Row)


    return Emote_List_Matrix



# Export/Write a CSV file that contains the information.
def Export_CSV(File_Name: str, Emote_Matrix = list) -> None:
    """
    Parameters
    ----------

    File_Name: str
        The name of the file which contains all the information that will be exported.
    Emote_Matrix: list
        List of emotes that the channel has.
        Order of items: [Channel, Emote_Name, Emote_URL]

    Returns
    -------
    
    None. It only does the action of exporting a CSV file.
    """

    import os, csv

    Export_Path = os.getcwd() + "\\" + File_Name + ".csv"

    header = ["Channel", "Emote_Name", "Emote_URL"]
    with open(Export_Path, "w", encoding="UTF8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(Emote_Matrix)


# Main method.
def main() -> None:
    import os

    "A Twitch Client ID Token and a Twitch Secret Token must exist as environment variables."
    Error_Message = "Error: no {} found. Please set an environment variable: {}"
    if not os.getenv("TWITCH_CLIENT_ID_TOKEN") or not os.getenv("TWITCH_SECRET_TOKEN"):
        print(Error_Message.format("Twitch Client ID Token missing."))
        print(Error_Message.format("Twitch Secret Token missing."))
    else:
        # Twitch credentials.
        _TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID_TOKEN")
        _TWITCH_SECRET = os.getenv("TWITCH_SECRET_TOKEN")

        # User list.
        _USERNAME_LIST = ["TwitchPresents", "Xbox"]

        # File name of the emote list.
        _FILE_NAME = "EmoteList"

        # Fetch the user list and the emote list from each channel.
        _USER_LIST = Get_User_ID_And_Name_From_List(Twitch_Client_ID = _TWITCH_CLIENT_ID, Twitch_Secret = _TWITCH_SECRET, User_List = _USERNAME_LIST)
        _EMOTE_LIST= Get_Emote_List(Twitch_Client_ID = _TWITCH_CLIENT_ID, Twitch_Secret = _TWITCH_SECRET, User_List = _USER_LIST)

        # Export a CSV with the information.
        Export_CSV(File_Name = _FILE_NAME, Emote_Matrix = _EMOTE_LIST)


# Run the main method.
if __name__ == '__main__':
    main()
