# #1. Ask user name, email ,phone,payment method
# #2. Ask users items to add to cart and price
# #3. Display total of the price
# #4. Order confirmed
# #5. Repeat if user want to purchase again

# user_name=input('Enter user name: ')
# email=input('Enter Email:')
# pay_meth=input('Enter payment method:')
# userDb={user:None
#         email:None
#         payment:None
#         cartList:None
#         Total:None
#        }
# userDb[user]=user_name
# userDb[email]=email
# userDb[payment]=pay_meth
# cart=[]
# total=0;
# while True:
#     product=input('Enter the product you want to add: ')
#     price=input('Price of product: ')
#     cart.append({product:price})
#     total=total+price
#     if 'y'==input('Enter y to enter more product else n-> y/n')
#       continue;
#     else:
#       userDb[cartList]=cart
#       break;

# userDb[Total]=total
# print(userDb)      



#1. Ask user name, email ,phone,payment method
#2. Ask users items to add to cart and price
#3. Display total of the price
#4. Order confirmed
#5. Repeat if user want to purchase again



user_name = input('Enter user name: ')
email = input('Enter Email: ')
pay_meth = input('Enter payment method: ')

userDb = {
        "user": user_name,
        "email": email,
        "payment": pay_meth,
        "cartList": [],
        "Total": 0
    }
cart = []
total = 0

while True:
        product = input('Enter the product you want to add: ')
        price = float(input('Price of product: '))

        cart.append({product: price})
        total += price

        choice = input('Enter y to enter more product else n -> y/n: ')
        if choice.lower() == 'y':
            continue
        else:
            break

        userDb["cartList"] = cart
        userDb["Total"] = total

        print("Order confirmed!")
        print(userDb)
     
        more = input("Do you want to purchase more? y/n: ")
        if again.lower() != 'y':
          break