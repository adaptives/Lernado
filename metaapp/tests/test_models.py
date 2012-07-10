from django.test import TestCase
from metaapp.models import *
from django.core.exceptions import ObjectDoesNotExist

class TestSidebarWidget(TestCase):
    
    
    def setUp(self):
        super(TestSidebarWidget, self).setUp()
        
    
    def tearDown(self):
        super(TestSidebarWidget, self).tearDown()
        
    
    def test_successfull_creation(self):
        SidebarWidget.objects.create(placement=1, title='test widget', contents='This is a simple widget')
        try:
            SidebarWidget.objects.get(placement=1, title='test widget')            
        except ObjectDoesNotExist: 
            self.fail('Could not find SidebarWidget after saving it')
            
    
    def test_unsuccessfull_creation(self):
        try:
            SidebarWidget.objects.create(placement=1, title='test widget')
            self.fail('Exception expected when a SidebarWidget is created without contents')
        except Exception: 
            pass
    