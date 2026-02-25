todo=[]
while True:

    inp=input("Add task :")
    todo.append(inp)
    if 'y'==input("Enter y to Add more tasks and n to stop-> y/n : ") :
        continue
    else:
        break    

print("TodoList")
print(todo)