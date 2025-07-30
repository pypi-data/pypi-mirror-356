# -------------------------------------------- #
#  ☢️ Note: please make sure you're editing    #
#  clients/custom_files/getopenpay/client.py   #
#                                              #
#  Other versions of this file will be         #
#  overwritten by the client generator.        #
# -------------------------------------------- #

from typing import NamedTuple

from getopenpay import ApiClient, Configuration


class ApiKeys(NamedTuple):
  publishable_key: str
  secret_key: str


class OpenPayClient:

  def __init__(self, api_keys: ApiKeys, host: str = 'https://connto.getopenpay.com'):
    self.api_keys = api_keys
    self.config = Configuration()
    self.config.host = host
    self.api_client = ApiClient(configuration=self.config)
    self.api_client.set_default_header('X-Publishable-Token', api_keys.publishable_key)
    self.api_client.set_default_header('Authorization', f'Bearer {api_keys.secret_key}')

  @property
  def accounts(self):
    # note these Apis are reinitialized everytime accounts are called.
    # they have lightweight inits for now
    from getopenpay.api import AccountsApi
    return AccountsApi(self.api_client)

  @property
  def authentication(self):
    from getopenpay.api import AuthenticationApi
    return AuthenticationApi(self.api_client)

  @property
  def product_bundles(self):
    from getopenpay.api import ProductBundlesApi
    return ProductBundlesApi(self.api_client)

  @property
  def coupons(self):
    from getopenpay.api import CouponsApi
    return CouponsApi(self.api_client)

  @property
  def credit_notes(self):
    from getopenpay.api import CreditNotesApi
    return CreditNotesApi(self.api_client)

  @property
  def users(self):
    from getopenpay.api import UsersApi
    return UsersApi(self.api_client)

  @property
  def customers(self):
    from getopenpay.api import CustomersApi
    from pydantic import BaseModel

    class OverriddenCustomersApi(CustomersApi):

      def list_customer_payment_methods(self, *args, **kwargs):
        result = super().list_customer_payment_methods(*args, **kwargs)

        if hasattr(result, 'data'):
          # Create a custom model to bypass validation
          class CustomListResponse(BaseModel):
            data: list
            total_objects: int
            page_number: int
            page_size: int

            class Config:
              arbitrary_types_allowed = True

          # Create a new instance of the custom model
          new_result = CustomListResponse(
            data=[
              item.actual_instance.actual_instance if hasattr(item, 'actual_instance')
              and hasattr(item.actual_instance, 'actual_instance') else
              item.actual_instance if hasattr(item, 'actual_instance') else item
              for item in result.data
            ],
            total_objects=result.total_objects,
            page_number=result.page_number,
            page_size=result.page_size
          )

          return new_result

        return result

    return OverriddenCustomersApi(self.api_client)

  @property
  def integrations(self):
    from getopenpay.api import IntegrationsApi
    return IntegrationsApi(self.api_client)

  @property
  def invites(self):
    from getopenpay.api import InvitesApi
    return InvitesApi(self.api_client)

  @property
  def invoice_items(self):
    from getopenpay.api import InvoiceItemsApi
    return InvoiceItemsApi(self.api_client)

  @property
  def invoices(self):
    from getopenpay.api import InvoicesApi
    return InvoicesApi(self.api_client)

  @property
  def payment_links(self):
    from getopenpay.api import PaymentLinksApi
    return PaymentLinksApi(self.api_client)

  @property
  def payment_methods(self):
    from getopenpay.api import PaymentMethodsApi

    class OverriddenPaymentMethodsApi(PaymentMethodsApi):

      def get_payment_method(self, *args, **kwargs):
        result = super().get_payment_method(*args, **kwargs)
        return result.actual_instance if hasattr(result, 'actual_instance') else result

    return OverriddenPaymentMethodsApi(self.api_client)

  @property
  def prices(self):
    from getopenpay.api import PricesApi
    return PricesApi(self.api_client)

  @property
  def products(self):
    from getopenpay.api import ProductsApi
    return ProductsApi(self.api_client)

  @property
  def promotion_codes(self):
    from getopenpay.api import PromotionCodesApi
    return PromotionCodesApi(self.api_client)

  @property
  def refunds(self):
    from getopenpay.api import RefundsApi
    return RefundsApi(self.api_client)

  @property
  def subscription_items(self):
    from getopenpay.api import SubscriptionItemsApi
    return SubscriptionItemsApi(self.api_client)

  @property
  def subscriptions(self):
    from getopenpay.api import SubscriptionsApi
    return SubscriptionsApi(self.api_client)

  @property
  def charges(self):
    from getopenpay.api import ChargesApi
    return ChargesApi(self.api_client)

  @property
  def events(self):
    from getopenpay.api import EventsApi
    return EventsApi(self.api_client)

  @property
  def transition_eligibility(self):
    from getopenpay.api import TransitionEligibilityApi
    return TransitionEligibilityApi(self.api_client)

  @property
  def checkout(self):
    from getopenpay.api import CheckoutApi
    return CheckoutApi(self.api_client)

  @property
  def product_family(self):
    from getopenpay.api import ProductFamilyApi
    return ProductFamilyApi(self.api_client)

  @property
  def billing_portal(self):
    from getopenpay.api import BillingPortalApi
    return BillingPortalApi(self.api_client)

  @property
  def tax_integrations(self):
    from getopenpay.api import TaxIntegrationsApi
    return TaxIntegrationsApi(self.api_client)

  @property
  def processor(self):
    from getopenpay.api import ProcessorsApi
    return ProcessorsApi(self.api_client)

  @property
  def webhook_utils(self):
    from getopenpay.utils.webhook_utils import WebhookUtils
    return WebhookUtils()

  @property
  def disputes(self):
    from getopenpay.api import DisputesApi
    return DisputesApi(self.api_client)

  @property
  def payment_intents(self):
    from getopenpay.api import PaymentIntentsApi
    return PaymentIntentsApi(self.api_client)

  @property
  def billing_meters(self):
    from getopenpay.api import BillingMetersApi
    return BillingMetersApi(self.api_client)

  @property
  def billing_meter_events(self):
    from getopenpay.api import BillingMeterEventsApi
    return BillingMeterEventsApi(self.api_client)

  @property
  def billing_meter_event_adjustments(self):
    from getopenpay.api import BillingMeterEventAdjustmentsApi
    return BillingMeterEventAdjustmentsApi(self.api_client)

  @property
  def single_use_tokens(self):
    from getopenpay.api import SingleUseTokensApi
    return SingleUseTokensApi(self.api_client)

  @property
  def payment_routes(self):
    from getopenpay.api import PaymentRoutesApi
    return PaymentRoutesApi(self.api_client)


# -------------------------------------------- #
#  ☢️ Note: please make sure you're editing    #
#  clients/custom_files/getopenpay/client.py   #
#                                              #
#  Other versions of this file will be         #
#  overwritten by the client generator.        #
# -------------------------------------------- #
