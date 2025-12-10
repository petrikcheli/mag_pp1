from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, FurnaceInputForm
from .models import FurnaceCalculation
from .blast import BlastFurnaceInput, IntermediateCalculations, HeatBalanceFull
from .utils import convert_result_keys
from django.db.models import Q
from django.template.loader import render_to_string

from xhtml2pdf import pisa

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()        

            return render(request,'registration/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'registration/register.html',{'user_form': user_form})

# @login_required
# def home_page(request):
#     result = None

#     if request.method == "POST":
#         form = FurnaceInputForm(request.POST)
#         if form.is_valid():
#             data = BlastFurnaceInput(**form.cleaned_data)
#             calc = HeatBalanceFull(data)
#             result = calc.get_balance()

#                         # Сохраняем расчет
#             FurnaceCalculation.objects.create(
#                 user=request.user,
#                 name=request.POST.get("calc_name") or None,  # можно добавить поле в форме
#                 input_data=form.cleaned_data,
#                 result_data=result
#             )
#     else:
#         form = FurnaceInputForm()

#     return render(request, "account/home_page.html", {
#         "section": "home_page",
#         "form": form,
#         "result": result
#     })


# @login_required
# def history_view(request):
#     calculations = FurnaceCalculation.objects.filter(user=request.user).order_by("-created_at")
#     return render(request, "account/history.html", {"calculations": calculations})

@login_required
def home_page(request):
    result_readable = None

    if request.method == "POST":
        form = FurnaceInputForm(request.POST)
        if form.is_valid():
            # --- создаем исходные данные ---
            bf_input = BlastFurnaceInput(**form.cleaned_data)

            # --- создаем промежуточные расчеты ---
            intermediate = IntermediateCalculations(bf_input)

            # --- создаем тепловой баланс с двумя объектами ---
            calc = HeatBalanceFull(bf_input, intermediate)
            result = calc.get_balance()

            # --- переименовываем поля результата ---
            result_readable = convert_result_keys(result)

            # --- сохраняем в историю ---
            FurnaceCalculation.objects.create(
                user=request.user,
                name=request.POST.get("calc_name") or None,
                input_data=form.cleaned_data,
                result_data=result_readable
            )
    else:
        form = FurnaceInputForm()

    return render(request, "account/home_page.html", {
        "section": "home_page",
        "form": form,
        "result": result_readable,  # передаем читаемый результат в шаблон
    })

@login_required
def history_view(request):
    query = request.GET.get("query", "").strip()

    calculations = FurnaceCalculation.objects.filter(user=request.user)

    if query:
        calculations = calculations.filter(
            Q(name__icontains=query)
        )

    calculations = calculations.order_by("-created_at")

    return render(request, "account/history.html", {
        "calculations": calculations,
        "query": query,
    })



@login_required
def delete_calculation(request, calc_id):
    calc = get_object_or_404(FurnaceCalculation, id=calc_id, user=request.user)
    if request.method == "POST":
        calc.delete()
        return redirect('history')
    return redirect('history')




@login_required
def pdf_calculation(request, calc_id):
    calc = get_object_or_404(FurnaceCalculation, id=calc_id, user=request.user)
    html = render_to_string("account/calculation_pdf.html", {"calc": calc})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="calculation_{calc.id}.pdf"'

    # Генерация PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status:
        return response
    return HttpResponse("Ошибка при генерации PDF", status=500)
    