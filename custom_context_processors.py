from lernado.metaapp.models import SidebarWidget

def sidebar_widgets(request):
    sidebar_widgets = SidebarWidget.objects.all().order_by('placement')
    return {'sidebar_widgets': sidebar_widgets}
