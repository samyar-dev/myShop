from shop.models import Product
import copy

class Cart:
    def __init__(self, request):
        self.session = request.session
        #here do not ignore
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart
        #until here
        self.save()

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
        else:
            self.cart[product_id]['quantity'] += 1
        self.save()

    def decrease(self, product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 0:
            self.cart[product_id]['quantity'] -= 1
        self.save()

    def remove(self, product):
        if product in self.cart:
            del self.cart[product]
            self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_post_price(self):
        post_price = sum(item['weight'] * item['quantity'] for item in self.cart.values())
        if post_price < 5:
            return 100000
        return 200000 
    
    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_copy = copy.deepcopy(self.cart)
        for product in products:
            cart_copy[str(product.id)]['product'] = product
        for item in cart_copy.values():
            yield item


    def save(self):
        self.session.modified = True