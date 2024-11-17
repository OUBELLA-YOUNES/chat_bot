import flet as ft
from flet import TextField, Row
import re
import random

def main(page: ft.Page):
    responses = [
        (r"\bbonjour\b|\bsalut\b|\bbnj\b|\bslt\b", [  "Salut! Comment allez-vous ?","Bonjour! Comment ça va ?"]),
        (r".*?\bbien\b.*?",[ "Ça fait plaisir à entendre , Comment puis-je vous aider aujourd'hui?" , "super ! ,Que puis-je faire pour vous ? "]),
        (r".*?\bton\b.*?\bnom\b.*?", "je suis votre ChatBot assistant, je suis là pour vous-aider!"),
        (r".*?\bdate\b.*\bconcours\b.*?", ["De quel concours exactement parlez-vous?", "de quelle spécialité parlez-vous"]),
        (r".*?Ing.*velop.*info.*", "Le concours du dev-info aura lieu        le  04 / 12 /2024 au forum "),
        (r".*?ing.*logiciel.*", "Le concours du génie logiciel aura lieu le 13 / 01 /2025 à la salle L2 ."),
        (r".*?souhaite?.*join.*", "absolument , Je n'ai besoin que d'un peu d'informations de votre part, pouvez-vous me fournir l'une de ces informations :           1-email | 2-numéro de telephone | 3-CNE"),
        
          
        (r".*?\bbye\b.*|.*\brevoir\b.*",["Bonne chance ! et j'espère avoir été utile , au revoir ! C'était sympa de discuter avec vous" ])
    ]

    expected_input = None

    def get_response(user_input):
         nonlocal expected_input
         if expected_input == "email":
            if re.fullmatch(r"^[a-zA-Z0-9_.+-]+@gmail\.[a-zA-Z]+$", user_input):
                expected_input = None  # réinitialiser après validation réussie
                return "Il semble que vous avez saisi une adresse gmail valide.Votre demande est en cours de traitement"
            else:
                return "Email invalide, veuillez saisir une adresse gmail correcte."
        
         elif expected_input == "telephone":
            if re.fullmatch(r"0[67]\d{8}", user_input):
                expected_input = None
                return "Il semble que vous avez saisi un numéro de téléphone valide.Votre demande est en cours de traitement"
            else:
                return "Numéro de téléphone invalide, veuillez saisir un numéro correct."
        
         elif expected_input == "CNE":
            if re.fullmatch(r'[a-z]\d{9}', user_input , re.IGNORECASE):
                expected_input = None
                return "Le CNE que vous avez saisi est valide.Votre demande est en cours de traitement"
            else:
                return "CNE invalide, veuillez saisir un CNE correct."

         for pattern, response in responses:
            if re.fullmatch(pattern, user_input.strip(), re.IGNORECASE):
                return random.choice(response) if isinstance(response, list) else response
         return "pourriez-vous formuler ce que vous dites"

    def send_message(e):
        nonlocal expected_input
        if input_zone.value:
            chat_log.content.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(f"Moi : {input_zone.value}", color=ft.colors.WHITE),
                            padding=10,
                            bgcolor=ft.colors.DEEP_PURPLE_500,
                            border_radius=10,
                            alignment=ft.alignment.center_left,
                            width=300,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
            )
            bot_response = get_response(input_zone.value)
            
            

            if input_zone.value.strip() == "1" or input_zone.value.strip().lower() == "email" :
                bot_response = "Vous avez choisi le choix 1. Veuillez insérer votre email."
                expected_input = "email"
            elif input_zone.value.strip() == "2" or input_zone.value.strip().lower() == "téléphone"  :
                bot_response = "Vous avez choisi le choix 2. Veuillez insérer votre numéro de téléphone."
                expected_input = "telephone"
            elif input_zone.value.strip() == "3" or input_zone.value.strip().lower() == "cne"  :
                bot_response = "Vous avez choisi le choix 3. Veuillez insérer votre code national d'étudiant (CNE)."
                expected_input = "CNE"
            elif expected_input and input_zone.value.strip() not in ["1", "2", "3"]:
                bot_response = f"Opération refusée : veuillez d'abord entrer un(e) {expected_input} valide."



            chat_log.content.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(f"Bot : {bot_response}", color=ft.colors.WHITE),
                            padding=10,
                            bgcolor=ft.colors.BLUE_GREY_700,
                            border_radius=10,
                            alignment=ft.alignment.center_left,
                            width=300,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            )            

                                                 
            input_zone.value = ""
            page.update()

    page.title = "Le Chatbot"
    page.window_width = 590
    page.window_height = 700
    page.window_resizable = False

   
    background_container = ft.Container(
        width=page.window_width,
        height=page.window_height,
        image_src="assets/image.jpg",  
        image_fit=ft.ImageFit.COVER
    )
    title = ft.Container(
        content=ft.Text(
            value=" bienvenue sur chatbot !",
            size=10,
            weight="bold",
            color=ft.colors.WHITE,
            text_align="center",
        ),
        alignment=ft.alignment.center,
        padding=5,
        border_radius=10,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["white", "black","white"]
        )
    )
    
    # Chat log container with a light semi-transparent background
    chat_log = ft.Container(
        content=ft.ListView(expand=True, spacing=5, padding=6, width=500, height=350, auto_scroll=True),
        border=ft.border.all(1, ft.colors.WHITE60),
        border_radius=10,
        padding=10,
        width=700,
        height=500,
        bgcolor=ft.colors.WHITE60
    )

    # Input field and send button
    input_zone = ft.TextField(
        hint_text="Chatez avec votre chatbot...",
        width=300,
        height=70,
        fill_color=ft.colors.LIGHT_BLUE_100,
        color=ft.colors.BLUE_GREY_900,
        hint_style=ft.TextStyle(color=ft.colors.BLUE_GREY_300),
        border_radius=20,
        border_color=ft.colors.DEEP_PURPLE_200,


        on_submit=send_message
    )

    send_button = ft.ElevatedButton(
        text="Envoyer",
        on_click=send_message,
        bgcolor=ft.colors.DEEP_PURPLE_500,
        color=ft.colors.WHITE,
        height= 40,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=20),
          
                        padding={"left": 15, "right": 15, "top": 10, "bottom": 10}  # Use a dictionary for padding

        )
    )

    
  # Main container with chat log and input field
    main_container = ft.Container(
    content=ft.Column(
        [
            title,
            chat_log,
            ft.Row(
                [input_zone, send_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Distribute elements with space between them
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    ),
    alignment=ft.alignment.top_center,  # Push everything slightly upwards
    padding=10,  # Reduce padding for better spacing
    width=580,  # Fixed width to maintain layout
    height=600,  # Fixed height
)



    # Use Stack to layer the background image behind the chat interface
    page.add(
        ft.Stack(
            controls=[
                background_container,  # Background image at the bottom
                main_container        # Chat interface on top
            ]
        )
    )

    page.update()

ft.app(target=main)
