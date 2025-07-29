
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

# Importar excepciones específicas de dominio
from apps.app1.domain.exceptions import EntityNotFoundError

# Importar formularios específicos de la entidad
from apps.app1.myentity_forms import MyentityCreateForm, MyentityEditGetForm, MyentityEditPostForm, MyentityViewForm

# Importar servicios específicos del dominio
from apps.app1.domain.services import (
    list_myentity,
    create_myentity,
    retrieve_myentity,
    update_myentity,
    delete_myentity,
)

# Importar repositorios específicos de la infraestructura
from apps.app1.infrastructure.myentity_repository import MyentityRepository


def myentity_list(request):
    """
    Vista genérica para mostrar una lista de todas las instancias de myentity.
    """

    myentityList = [] #inicialize list

    # Obtener la lista del repositorio
    try:
        repository = MyentityRepository()
        myentityList = list_myentity(repository=repository)

    except ValueError as e:
        # Manejo de errores específicos del dominio
        messages.error(request,  str(e))

    # Renderizar la plantilla con la lista
    return render(request, 'apps/app1/myentity_web_list.html', {
        'myentityList': myentityList
    })


def myentity_create(request):
    """
    Vista genérica para crear una nueva instancia de myentity utilizando un servicio.
    """

    if request.method == "POST":

        # Validar los datos del formulario
        form = MyentityCreateForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data
            repository = MyentityRepository()

            # Obtener el ID de la entidad relacionada si existe
            parent_id = request.POST.get('parent_id', None)

            try:
                # LLamar al servicio de creación
                create_myentity(repository=repository, parent_id=parent_id, data=form_data)

                # Mostrar mensaje de éxito y redirigir
                messages.success(request, f"Successfully created myentity.")
                return redirect('apps:app1:myentity_list')

            except ValueError as e:
                # Manejar errores específicos del dominio
                form.add_error(None, str(e))
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        # Formulario vacío para solicitudes GET
        form = MyentityCreateForm()

    # Renderizar la plantilla con el formulario
    return render(request, 'apps/app1/myentity_web_create.html', {'form': form}) 


def myentity_edit(request, id=None):
    """
    Vista genérica para editar una instancia existente de myentity utilizando un servicio.
    """

    if id is None:
        # Redireccion si no se proporciona un ID
        return redirect('apps:app1:myentity_list')

    repository = MyentityRepository()

    try:
        # Obtener los datos de la entidad desde el servicio
        myentity = retrieve_myentity(repository=repository, entity_id=id)

    except EntityNotFoundError as e:
        # Manejar errores específicos del dominio
        messages.error(request,  str(e))
        return redirect('apps:app1:myentity_list')

    except ValueError as e:
        # Manejar errores específicos del dominio
        messages.error(request,  str(e))
        return redirect('apps:app1:myentity_list')

    if request.method == "POST":

        # Validar los datos del formulario
        form = MyentityEditPostForm(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data

            try:
                # obtenemos del request los campos especiales del formulario
                # ejemplo: password = request.POST.get('password', None)
                # ejemplo: photo = request.FILES.get('photo', None)
                # y los enviamos como parametros al servicio de actualizacion

                # LLamar al servicio de actualización
                update_myentity(repository=repository, entity_id=id, data=form_data)

                # Mostrar mensaje de éxito
                messages.success(request, f"Successfully updated myentity.")

                # Redireccionar a la lista de myentitys
                return redirect('apps:app1:myentity_list')

            except EntityNotFoundError as e:
                form.add_error(None, str(e))

            except ValueError as e:
                form.add_error(None, str(e))

        else:
            messages.error(request, "There were errors in the form. Please correct them.")

    # request.method == "GET":
    else:  
        # Initialize the form with existing data
        form = MyentityEditGetForm(initial={
            'id': myentity['id'],            
            'name': myentity['name'],
            'email': myentity['email']
        })

    # Renderizar la plantilla con el formulario
    return render(request, 'apps/app1/myentity_web_edit.html', {'form': form})


def myentity_detail(request, id=None):
    """
    Vista genérica para mostrar los detalles de una instancia específica de myentity.
    """
    if id is None:
        return redirect('apps:app1:myentity_list')

    repository = MyentityRepository()
    try:
        # Obtener los datos de la entidad desde el servicio
        myentity = retrieve_myentity(repository=repository, entity_id=id)

    except EntityNotFoundError as e:
        # Manejar errores específicos del dominio
        messages.error(request,  str(e))
        return redirect('apps:app1:myentity_list')

    except ValueError as e:
        # Manejar errores específicos del dominio
        messages.error(request,  str(e))
        return redirect('apps:app1:myentity_list')

    # Renderizar la plantilla con el formulario de vista
    form = MyentityViewForm(initial={
        'name': myentity['name'],
        'email': myentity['email']
    })

    return render(request, 'apps/app1/myentity_web_detail.html', {'form': form})


def myentity_delete(request, id=None):
    """
    Vista genérica para eliminar una instancia existente de myentity utilizando un servicio.
    """
    if id is None:
        messages.error(request, "Non Valid id to delete")
        return redirect('apps:app1:myentity_list')

    repository = MyentityRepository()
    try:
        # LLamar al servicio de eliminación
        delete_myentity(repository=repository, entity_id=id)
        messages.success(request, f"Successfully deleted myentity.")

    except EntityNotFoundError as e:
        # Manejar errores específicos del dominio
        messages.error(request,  str(e))
        
    except ValueError as e:
        # Manejar errores específicos del dominio
        messages.error(request,  str(e))

    return redirect('apps:app1:myentity_list')

