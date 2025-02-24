from django.shortcuts import render,redirect,get_object_or_404
import random
from django.http import JsonResponse
import time
from .models import Profile,MoneyCode,Store,Product
from django.contrib.auth.hashers import check_password
from django.contrib import messages

from django.core.paginator import Paginator
from .models import Galeri,Quiz
from random import choice
from django.utils.cache import patch_cache_control
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

USERNAME = 'User' # Type a username as you wish 
PASSWORD_HASH = "" # password but not a hashed one 
SECRET_ENTRANCE = "" # A gallery where you can store images and SECRET_ENTRANCE is the password for it 

class QuestionObject:
    def __init__(self, text, options, correct_index):
        self.text = text
        self.options = options
        self.correct_index = correct_index

def get_gold(request):
    if request.method == "GET":
        gold = request.session.get("gold", 100)
        return JsonResponse({"gold": gold}) 

    return JsonResponse({"error": "Invalid request"}, status=400)


def update_gold(gold):
    object = Profile.objects.get(username = 'User')
    object.gold = gold
    object.save()
    


#HELP SECTION
def help(request):
    gold = request.session['gold']
    update_gold(gold=gold)

    return render(request,'help.html',{'gold':gold})

def money_req(request):
    object = Profile.objects.get(username='User')  
    gold = request.session.get('gold', object.gold) 
    object.gold = gold  
    object.save(update_fields=['gold']) 

   
    code_objects = MoneyCode.objects.filter(achived=False)
    code_objects_list = list(code_objects.values_list('code', flat=True)) 

    print(code_objects_list)  

    if request.method == 'POST':
        code = request.POST.get('money_code').upper()
        print(code)  

        if code in code_objects_list:
            object.gold += 100 
            object.save(update_fields=['gold']) 

           
            request.session['gold'] = object.gold

            code_objects.filter(code=code).update(achived=True)
            return render(request,'home.html', {'gold': gold})

    return render(request, 'money_request.html', {'gold': gold})

#HELP SECTION

#PROFILE
def secret_entrance(request):
    gold = request.session.get('gold', 100)  
    update_gold(gold=gold)

    error_message = None 
    if request.method == 'POST':
        password = request.POST.get('password')

        if password == SECRET_ENTRANCE:
            print(f'{password} {SECRET_ENTRANCE}')
            return redirect('galeri')
        else:
            print(f'{password} {SECRET_ENTRANCE}')
            error_message = "❌ Wrong password! Try again."  
            return redirect('secret_entrance')

    return render(request, 'secret_entrance.html', {'gold': gold, 'error_message': error_message})

#PROFILE

#GALERI



def gallery_view(request):
    gold = request.session['gold']
    update_gold(gold=gold)

    photos = Galeri.objects.all().order_by('-id')  
    paginator = Paginator(photos, 9)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "galeri.html", {"photos": page_obj})


def upload(request):
    gold = request.session['gold']
    update_gold(gold=gold)

    if request.method == "POST":
        images = request.FILES.getlist('images')
        uploaded_files = []  

        if not images:
            return JsonResponse({"error": "Hiç dosya seçilmedi!"}, status=400)

        for image in images:
            photo = Galeri.objects.create(image=image)
            uploaded_files.append({"url": photo.image.url})  

        return JsonResponse({"message": "Başarıyla yüklendi!", "uploaded_files": uploaded_files})

    
    return JsonResponse({"error": "Geçersiz istek!"}, status=400)



#GALERI


def index(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        print(PASSWORD_HASH)
        print(password)

        if password == PASSWORD_HASH:
            request.session['authenticated'] = True
            return redirect('home')
        else:
            messages.error(request,f'Hatali Sifre')
            return render(request,'index.html',{'hide_navbar': True})
        
    return render(request, 'index.html',{'hide_navbar': True} )



def home(request):
    if not request.session.get('authenticated'):
        return redirect('index')
    object = Profile.objects.get(username = 'User')
    print(object.gold)
    gold = object.gold


    request.session['gold'] = gold
    
    return render(request, 'home.html', {'gold':gold})

def pref(request):
    gold = request.session['gold']
    update_gold(gold=gold)

    return render(request,'pref.html', {'gold':gold})



def decide_for_me(request):
    gold = request.session['gold']
    update_gold(gold=gold)

    if request.method == 'POST':
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')

        result = random.choice(['heads', 'tails'])
        chosen_option = option1 if result == 'heads' else option2
        

        return render(request, 'decide_for_me.html', {
            'result': result,
            'chosen_option': chosen_option,
            'gold':gold
            
        })
    return render(request, 'decide_for_me.html',{'gold':gold})


def product(request):
    gold = request.session.get('gold', 100)  
    update_gold(gold=gold)
    request.session['gold'] = gold

    products = Product.objects.all()

    return render(request, 'product.html', {'gold': gold, 'products': products})


def delete_product(request, id):
    gold = request.session.get('gold', 100)
    update_gold(gold=gold)
    request.session['gold'] = gold

    deleted_product = get_object_or_404(Product, pk=id)
    deleted_product.delete()

    return redirect('product')


def new_product(request):
    gold = request.session.get('gold', 100)
    update_gold(gold=gold)
    request.session['gold'] = gold

    if request.method == "POST":
        product_name = request.POST.get("product_name")
        prdouct_type = request.POST.get("product_type")
        product_price = request.POST.get("product_price")
        product_link = request.POST.get("product_link")

        if product_name and product_price:
            Product.objects.create(
                product_name=product_name,
                product_type=prdouct_type,
                product_price=product_price,
                product_link=product_link
            )
            return redirect('product')

    return render(request, "new_product.html", {"gold": gold})
    

## GAME GAMES SECTION ##
def gamble(request):
    gold = request.session['gold']
    update_gold(gold=gold)

    return render(request,'gamble.html' , {'gold':gold})

def rps(request):
    gold = request.session.get('gold', 100)  # Get user's current gold
    request.session['gold'] = gold  
    update_gold(gold=gold)

    if request.method == 'POST':
        try:
            bet_amount = float(request.POST.get('bet_amount', 0))
            final_amount = float(request.POST.get('final_amount', 0))  

           
            if bet_amount > gold:
                return JsonResponse({'error': 'Yetersiz bakiye!'}, status=400)
            
           
            gold += final_amount
            update_gold(gold=gold)  
            request.session['gold'] = gold  

            print(f"🎲 RPS Game: Bet = {bet_amount}, Win/Loss = {final_amount}, New Balance = {gold}")

            return JsonResponse({'message': f'Bakiyeniz güncellendi: {gold}', 'new_gold': gold})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'rps.html', {'gold': gold})



def slot(request):
    gold = request.session.get('gold', 100)
    request.session['gold'] = gold 
    update_gold(gold=gold)
    if request.method == 'POST':
        bet_amount = float(request.POST.get('bet_amount', 0))
        final_amount = float(request.POST.get('final_amount', 0))  
        
       
        gold += final_amount
        update_gold(gold)
        request.session['gold'] = gold  

        print(f"Bahis: {bet_amount}, Kazanç/Kayıp: {final_amount}, Güncel Bakiye: {gold}")

        return render(request, 'gamble.html', {'gold': gold})

        

    return render(request, 'slot.html', {'gold': gold})


def baccarat(request):
    gold = request.session.get('gold', 100)  
    
    if request.method == 'POST':
        bet_amount = float(request.POST.get('bet_amount', 0))
        final_amount = float(request.POST.get('final_amount', '0')) 
        
        
        gold += final_amount
        request.session['gold'] = gold  

       
        update_gold(gold)

        print(f"Bahis: {bet_amount}, Kazanç/Kayıp: {final_amount}, Güncel Bakiye: {gold}")

        return JsonResponse({'message': f'Bakiyeniz güncellendi: {gold}'})

    return render(request, 'baccarat.html', {'gold': gold})



#STORE
def store(request):
    gold = request.session.get('gold', 100) 
    update_gold(gold=gold) 

    store_objects = Store.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_id = int(request.POST.get('product_id'))
        print(f"Seçilen Ürün: {product_name} (ID: {product_id})")  
        selected_product = Store.objects.get(pk=product_id)
        selected_product_type = selected_product.product_type
        print(selected_product_type)
        if gold < selected_product.product_price:
            print(f'Yetersiz bakiye {gold} ve {selected_product.product_price}')
        else:
            if selected_product_type: # GORSEL
                image = selected_product.image
                galeri_object = Galeri.objects.create(
                    image = image
                )
                galeri_object.save()
                selected_product.achived = True
                selected_product.save()

                gold -= selected_product.product_price
                request.session['gold'] = gold
                update_gold(gold)
                return render(request,'purchase_completed.html',{'gold': gold, 'product':selected_product})


            else:
                selected_product.achived = True
                gold -= selected_product.product_price
                request.session['gold'] = gold
                update_gold(gold)
                
                selected_product.save()

                return render(request,'purchase_completed.html',{'gold': gold, 'product':selected_product})



    return render(request, 'store.html', {'gold': gold, 'store': store_objects})

def purchase_completed(request):

    gold = request.session.get('gold', 100)
    request.session['gold'] = gold 
    update_gold(gold=gold) 



    return render(request,'purchase_completed.html',{'gold': gold,})



#STORE





#QUIZ
def quiz_menu(request):
    gold = request.session.get('gold', 100)
    request.session['gold'] = gold 
    update_gold(gold=gold) 

    quiz_objects = Quiz.objects.all()
    print(quiz_objects)



    return render(request,'quiz_menu.html',{'gold': gold , 'quiz_objects':quiz_objects})




def quiz(request, id):
    gold = request.session.get('gold', 100)
    request.session['gold'] = gold 
    update_gold(gold=gold)

    user_answers = []
    real_answers = []
    quiz = get_object_or_404(Quiz, pk=id)
    questions = [QuestionObject(q["text"], q["options"], q["correct_index"]) for q in quiz.questions]

    for i in questions:
        real_answers.append(i.correct_index)

    if request.method == "POST":
        for index, question in enumerate(questions, start=1):
            question_key = f"question_{index}"  
            selected_option = request.POST.get(question_key)

            if selected_option is None:
                continue  

            user_answers.append(int(selected_option))  

        if not user_answers:
            print('No Answers Provided')
        else:
            correct_list = [real == user for real, user in zip(real_answers, user_answers)]
            how_many_correct = sum(correct_list)
            prize = how_many_correct * 40  

            quiz.status = True
            quiz.save()

            gold += prize
            update_gold(gold=gold)
            request.session['gold'] = gold 

            return redirect('result', prize=prize, how_many_correct=how_many_correct)

    return render(request, 'quiz.html', {'gold': gold, 'quiz': quiz, 'questions': questions})


def result(request, prize, how_many_correct):
    gold = request.session.get('gold', 100)

    return render(request, 'result.html', {
        'prize': prize,
        'how_many_correct': how_many_correct,
        'gold': gold
    })


#QUIZ