from django.shortcuts import render
from django.http import JsonResponse
from .models import ChatMessage

def chatbot(request):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    if request.method == 'POST':
        user = request.POST.get('user')
        message = request.POST.get('message')
        ChatMessage.objects.create(user=user, message=message)
        # Add the message to the chat history stored in the session
        request.session['chat_history'].append({'user': user, 'message': message})
        
        # Add your chatbot logic here and get a response
        response = get_manual_response(message)
        # Add the chatbot response to the chat history stored in the session
        request.session['chat_history'].append({'user': 'Chatbot', 'message': response})

        return JsonResponse({'response': response})

    # Pass the chat history to the template
    chat_history = request.session.get('chat_history', [])
    return render(request, 'chatbot/chat.html', {'chat_history': chat_history})


def get_manual_response(user_input):
    # Add more response logic based on common e-commerce queries
    if "product" in user_input.lower():
        return "Sure, let me help you find the perfect product!"
    elif "order" in user_input.lower():
        return "How can i assist you with order-related queries."
    elif "discount" in user_input.lower():
        return "We have some exciting discounts available! ONLY ON COUPON CODES"
    elif "delivery" in user_input.lower():
        return "Our standard delivery time is 3-5 business days. Express delivery is available for an additional fee."
    elif "return" in user_input.lower():
        return "For information on returns and refunds, please visit our 'About US' page on the website."
    elif "payment" in user_input.lower():
        return "We accept various payment methods, including credit cards, UPI, and more. You can find details during checkout."
    elif "pay" in user_input.lower():
        return "We accept various payment methods, including credit cards, UPI, and more. You can find details during checkout."
    elif "account" in user_input.lower():
        return "To manage your account, log in to your profile. You can update personal information, track orders, and more."
    elif "hey" in user_input.lower():
        return "hey,How can I assist you today?"
    elif "hello" in user_input.lower():
        return "hello,How can I assist you today?"
    elif "hi" in user_input.lower():
        return "hii,How can I assist you today?"
    else:
        return "I'm sorry, I didn't understand that. How can I assist you today?"
