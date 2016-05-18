import itertools

from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView

from stylist.forms import MyUserCreationForm
from stylist.models import Item


class SignUpView(CreateView):
    """Collect user data and retrieve woeid for given zip code."""

    form_class = MyUserCreationForm
    template_name = 'stylist/signup.html'
    success_url = reverse_lazy('login')


class MyItems(ListView):
    """List items owned by logged user."""
    
    model = Item
    template_name = 'stylist/my_items.html'

    def get_queryset(self):
        return super(MyItems, self).get_queryset().filter(owner=self.request.user)


class AddItem(CreateView):
    """Add item to logged user's wardrobe."""

    model = Item
    success_url = reverse_lazy('my_items')
    fields = ['item_type', 'color', 'temperature']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AddItem, self).form_valid(form)


class RemoveItem(DeleteView):
    """Remove item from logged user's wardrobe."""

    model = Item
    success_url = reverse_lazy('my_items')

    def get_queryset(self):
        return super(RemoveItem, self).get_queryset().filter(owner=self.request.user)


class MyForecast(TemplateView):
    """Retrieve today's forecast for user's location, display set of clothes from user's wardrobe.
    
    Choose clothes based on availability, temperature and matching colors.
    """

    get_template_name = "stylist/forecast.html"
    post_template_name = "stylist/what_to_wear.html"

    def get_template_names(self):
        return [{'GET': self.get_template_name, 'POST': self.post_template_name}[self.request.method]]

    def what_to_wear(self, low, high):
        """Return best scored combination of clothes for given temperatures."""

        high_classification = Item.classify_temperature(high)
        tops = self.request.user.item_set.filter(item_type__in=Item.TOPS, temperature=high_classification)
        bottoms = self.request.user.item_set.filter(item_type__in=Item.BOTTOMS, temperature=high_classification)
        outers = []
        if high - low >= Item.DIURNAL_VARIATION or high_classification == Item.COLD:
            outers = self.request.user.item_set.filter(item_type__in=Item.OUTERS, temperature=high_classification)

        def score(top, bottom, outer):
            """Score given set of clothes based on colors."""
            colors = [top.color, bottom.color]
            if outer:
                colors.append(outer.color)
            return Item.COLOR_SET_SCORES[frozenset(colors)]

        combinations = list(itertools.product(tops, bottoms, outers or [None]))
        combinations.sort(lambda x, y: cmp(score(*y), score(*x)))
        return combinations[0] if combinations else ()

    def get_context_data(self, **kwargs):
        context = super(MyForecast, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            low = int(self.request.POST["low"])
            high = int(self.request.POST["high"])
            context["low"] = low
            context["high"] = high
            context["clothes"] = self.what_to_wear(low, high)
        else:
            context['woeid'] = self.request.user.woeid
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
