from django.shortcuts import render

def home(request):
	usuario = ''
	return render (request, 'core/home.html', { 'usuario': usuario })
