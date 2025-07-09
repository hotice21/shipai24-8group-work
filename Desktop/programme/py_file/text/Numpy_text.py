from numpy.lib.polynomial import roots


class link_1:
    def __init__(self,val):
        self.next=None
        self.val=val

def return_kth_to_last(root,k,n=1,root2=None):
    if n<k:
        return return_kth_to_last(root.next,k,n+1,root)
    else:
        if root.next != None:
            return return_kth_to_last(root.next,k,n,root2.next)
        else:
            return root2

def delete_middle_node(root,targe):
    if root.val!=targe:
        if root.next.val != targe:
            delete_middle_node(root.next,targe)
        else:
            root.next=root.next.next
    else:
        root.next=None
    return 0

def reverse_link(root,next=None):
    last=next
    if root.next!=None:
        last=reverse_link(root.next,root)
    root.next=last
    return next

class _DoublyLinkedBase:
    def __init__(self,val=None):
        self.val=val
        self.next=None
        self.prev=None

    def reverse_list(self,root):
        if root.next!=None:
            self.reverse_list(root.next)
        root.next,root.prev=root.prev,root.next

if __name__ =="__main__":
    import datetime
    print(datetime.datetime.now())
    """l=[link_1(0)]
    for i in range(1,10):
        temp=link_1(i)
        l[i-1].next=temp
        l.append(temp)
    a=0
    temp=l[0]
    while a!=10:
        a+=1
        print(temp.val)
        temp=temp.next"""