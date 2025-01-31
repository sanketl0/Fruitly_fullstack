from django.urls import path, include

from rest_framework.routers import SimpleRouter
from . import views
from . import viewsets

router = SimpleRouter()
router.register('AccountStatement', viewsets.AccountStatementViewSet, basename='AccountStatement')
router.register('TransactionStatus', viewsets.TransactionStatusViewSet, basename='TransactionStatus')
router.register('TransactionInitiation', viewsets.TransactionInitiationViewSet, basename='TransactionInitiation')
router.register('UAT', viewsets.UATViewSet, basename='UAT')
router.register('Balance', viewsets.BalanceViewSet, basename='Balance')
router.register('BankServerSync', viewsets.BankServerSyncViewSet, basename='BankServerSync')
router.register('Transactions', viewsets.TransactionViewSet, basename='Transactions')

urlpatterns = [
    path('', include(router.urls)),

]
