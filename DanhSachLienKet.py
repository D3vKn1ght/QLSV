from unidecode import unidecode


def compareName(name1, name2):
    name1 = unidecode(name1).lower().split(' ')
    name2 = unidecode(name2).lower().split(' ')
    i = 1
    while i <= len(name1) and i <= len(name2):
        if name1[len(name1)-i] > name2[len(name2)-i]:
            return 1
        elif name1[len(name1)-i] < name2[len(name2)-i]:
            return -1
        i += 1
    return 0


def compare(list1, list2, key):
    if key == 0 or key == 1 or key == 4:
        if list1[key] > list2[key]:
            return 1
        elif list1[key] < list2[key]:
            return -1
        return 0
    elif key == 3:
        date1 = int("".join(list1[3].split("/")[::-1]))
        date2 = int("".join(list2[3].split("/")[::-1]))
        if date1 > date2:
            return 1
        elif date1 < date2:
            return -1
        return 0
    elif key == 2:
        return compareName(list1[2], list2[2])
    return 0


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:

    def __init__(self):
        self.head = None
        self.isSorted = -1

    def getBeginNode(self):
        return self.head

    def getEndNode(self):
        temp = self.head
        while (temp.next):
            temp = temp.next
        return temp

    def printList(self):
        temp = self.head
        while (temp):
            print(temp.data)
            temp = temp.next

    def push(self, new_data):
        self.isSorted = -1
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node

    def insertAfter(self, prev_node, new_data):
        self.isSorted = -1
        if prev_node is None:
            print("The given previous node must in Linked List")
            return
        new_node = Node(new_data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def append(self, new_data):
        self.isSorted = -1
        new_node = Node(new_data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while (last.next):
            last = last.next
        last.next = new_node

    def deleteNode(self, key):
        temp = self.head
        if (temp is not None):
            if (temp.data == key):
                self.head = temp.next
                temp = None
                return
        while (temp is not None):
            if temp.data == key:
                break
            prev = temp
            temp = temp.next
        if (temp == None):
            return
        prev.next = temp.next
        temp = None

    def deleteNodeAt(self, position):
        if self.head == None:
            return
        temp = self.head
        if position == 0:
            self.head = temp.next
            temp = None
            return
        for i in range(position - 1):
            temp = temp.next
            if temp is None:
                break
        if temp is None:
            return
        if temp.next is None:
            return
        next = temp.next.next
        temp.next = None
        temp.next = next

    def deleteList(self):
        temp = self.head
        while (temp):
            next = temp.next
            del temp.data
            temp = next
        self.head = None
        self.isSorted = -1

    def search(self, x):
        temp = self.head
        while (temp):
            if temp.data == x:
                return True
            temp = temp.next
        return False

    def Length(self):
        temp = self.head
        count = 0
        while (temp):
            count += 1
            temp = temp.next
        return count

    def swapNodesAt(self, position1, position2):
        temp1 = self.getNode(position1)
        temp2 = self.getNode(position2)
        temp1.data, temp2.data = temp2.data, temp1.data

    def getNode(self, position):
        temp = self.head
        if position == 0:
            return temp
        for i in range(position):
            temp = temp.next
            if temp is None:
                break
        return temp

    def insertionSort(self, key):
        if self.head is None:
            return
        temp1 = self.head.next
        while temp1:
            temp2 = self.head
            while temp2 != temp1 and compare(temp2.data, temp1.data, key) <= 0:
                temp2 = temp2.next
            temp3 = temp2
            lst = [temp1.data]
            while temp3 != temp1:
                lst.append(temp3.data)
                temp3 = temp3.next
            for i in lst:
                temp2.data = i
                temp2 = temp2.next
            temp1 = temp1.next
        self.isSorted = key

    def bubbleSort(self, key):
        if self.head is None:
            return
        while True:
            check = False
            temp = self.head
            while(temp.next):
                if compare(temp.data, temp.next.data, key) > 0:
                    temp.data, temp.next.data = temp.next.data, temp.data
                    check = True
                temp = temp.next
            if not check:
                break
        self.isSorted = key

    def selectionSort(self, key):
        if self.head is None:
            return
        temp1 = self.head
        while temp1.next:
            min_node = temp1
            temp2 = temp1.next
            while temp2:
                if compare(temp2.data, min_node.data, key) < 0:
                    min_node = temp2
                temp2 = temp2.next
            temp1.data, min_node.data = min_node.data, temp1.data
            temp1 = temp1.next
        self.isSorted = key

    def quickSortByList(self, lst, start, end, key):
        if start >= end:
            return
        pivot = lst[start]
        left = start + 1
        right = end
        while left <= right:
            while left <= right and compare(lst[left], pivot, key) <= 0:
                left += 1
            while left <= right and compare(lst[right], pivot, key) > 0:
                right -= 1
            if left <= right:
                lst[left], lst[right] = lst[right], lst[left]
                left += 1
                right -= 1
        lst[start], lst[right] = lst[right], lst[start]
        self.quickSortByList(lst, start, right - 1, key)
        self.quickSortByList(lst, right + 1, end, key)

    def quickSort(self, lst, key):
        if lst is None:
            return
        self.quickSortByList(lst, 0, len(lst) - 1, key)
        self.listToLinkedList(lst)
        self.isSorted = key

    def mergeSortByList(self, lst, start, end, key):
        if start >= end:
            return
        mid = (start + end) // 2
        self.mergeSortByList(lst, start, mid, key)
        self.mergeSortByList(lst, mid + 1, end, key)
        temp = []
        left = start
        right = mid + 1
        while left <= mid and right <= end:
            if compare(lst[left], lst[right], key) <= 0:
                temp.append(lst[left])
                left += 1
            else:
                temp.append(lst[right])
                right += 1
        while left <= mid:
            temp.append(lst[left])
            left += 1
        while right <= end:
            temp.append(lst[right])
            right += 1
        for i in temp:
            lst[start] = i
            start += 1

    def mergeSort(self, lst, key):
        if lst is None:
            return
        self.mergeSortByList(lst, 0, len(lst) - 1, key)
        self.listToLinkedList(lst)
        self.isSorted = key

    def linearSearch(self, data, key):
        answer = []
        check = False
        temp = self.head
        while temp:
            if compare(temp.data, [data]*5, key) == 0:
                answer.append(temp.data)
                check = True
            temp = temp.next
        if not check:
            return None
        return answer

    def quickSortByLinkedList(self, start, end, key):
        if start >= end:
            return
        pivot = self.getNode(start)
        left = start + 1
        right = end
        while left <= right:
            while left <= right and compare(self.getNode(left).data, pivot.data, key) <= 0:
                left += 1
            while left <= right and compare(self.getNode(right).data, pivot.data, key) > 0:
                right -= 1
            if left <= right:
                self.getNode(left).data, self.getNode(right).data = self.getNode(
                    right).data, self.getNode(left).data
                left += 1
                right -= 1
        self.getNode(start).data, self.getNode(right).data = self.getNode(
            right).data, self.getNode(start).data
        self.quickSortByLinkedList(start, right - 1, key)
        self.quickSortByLinkedList(right + 1, end, key)

    def mergeSortByLinkedList(self, start, end, key):
        if start >= end:
            return
        mid = (start + end) // 2
        self.mergeSortByLinkedList(start, mid, key)
        self.mergeSortByLinkedList(mid + 1, end, key)
        i = start
        j = mid + 1
        temp = []
        while i <= mid and j <= end:
            if compare(self.getNode(i).data, self.getNode(j).data, key) <= 0:
                temp.append(self.getNode(i).data)
                i += 1
            else:
                temp.append(self.getNode(j).data)
                j += 1
        while i <= mid:
            temp.append(self.getNode(i).data)
            i += 1
        while j <= end:
            temp.append(self.getNode(j).data)
            j += 1
        i = start
        j = 0
        while i <= end:
            self.getNode(i).data = temp[j]
            i += 1
            j += 1

    def binarySearch(self, lst, data, key, answer):
        min = 0
        max = len(lst)-1
        avg = min+(max-min)//2
        while(min <= max):
            if (compare(lst[avg], [data]*5, key) == 0):
                answer.append(lst[avg])
                return self.binarySearch(lst[:avg], data, key, answer), self.binarySearch(lst[avg+1:], data, key, answer)
            elif(compare(lst[avg], [data]*5, key) > 0):

                return self.binarySearch(lst[:avg], data, key, answer)
            else:
                return self.binarySearch(lst[avg+1:], data, key, answer)

    def getBinarySearch(self, lst, data, key):

        answer = []
        # print(lst)
        self.binarySearch(lst, data, key, answer)
        if(len(answer) == 0):
            return None
        return answer

    def listToLinkedList(self, lst):
        temp = self.head
        for data in lst:
            temp.data = data
            temp = temp.next
        temp = None

    def statisticsAccordingToLearningResults(self, className):
        dic = {"XuatSac": 0, "Gioi": 0, "Kha": 0,
               "TrungBinh": 0, "Yeu": 0, "Kem": 0}
        temp = self.head
        while temp:
            if temp.data[4] >= 9 and temp.data[0] == className:
                dic["XuatSac"] += 1
            elif temp.data[4] >= 8 and temp.data[4] < 9 and temp.data[0] == className:
                dic["Gioi"] += 1
            elif temp.data[4] >= 7 and temp.data[4] < 8 and temp.data[0] == className:
                dic["Kha"] += 1
            elif temp.data[4] >= 6 and temp.data[4] < 7 and temp.data[0] == className:
                dic["TrungBinh"] += 1
            elif temp.data[4] >= 5 and temp.data[4] < 6 and temp.data[0] == className:
                dic["Yeu"] += 1
            elif temp.data[4] >= 0 and temp.data[4] < 5 and temp.data[0] == className:
                dic["Kem"] += 1
            temp = temp.next
        return dic

    def getStatisticsAccordingToLearningResults(self):  # Thong ke theo diem
        dic = {}
        temp = self.head
        while temp:
            if temp.data[0] not in dic:
                dic[temp.data[0]] = self.statisticsAccordingToLearningResults(
                    temp.data[0])
            temp = temp.next
        # return dic
        sort_dic = {}

        for i in sorted(dic):
            sort_dic.update({i: dic[i]})
        sum = {"XuatSac": 0, "Gioi": 0, "Kha": 0,
               "TrungBinh": 0, "Yeu": 0, "Kem": 0}
        for i in sort_dic:
            sum["XuatSac"] += sort_dic[i]["XuatSac"]
            sum["Gioi"] += sort_dic[i]["Gioi"]
            sum["Kha"] += sort_dic[i]["Kha"]
            sum["TrungBinh"] += sort_dic[i]["TrungBinh"]
            sum["Yeu"] += sort_dic[i]["Yeu"]
            sum["Kem"] += sort_dic[i]["Kem"]
        sort_dic.setdefault("Tong", sum)
        return sort_dic

    def statisticAccordingToGrade(self):  # Thong le theo lop
        dic = {}
        temp = self.head
        while temp:
            if temp.data[0] not in dic:
                dic[temp.data[0]] = 1
            else:
                dic[temp.data[0]] += 1
            temp = temp.next
        return dic
