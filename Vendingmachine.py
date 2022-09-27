# 품목샘플
juice = {1: {'이름': 'pepsi', '원가': 1200, '정가': 1800, '수량': 5, '무게': 15},
         2: {'이름': 'zeropepsi', '원가': 1300, '정가': 1800, '수량': 5, '무게': 15},
         3: {'이름': 'cocacola', '원가': 1500, '정가': 1800, '수량': 5, '무게': 15},
         4: {'이름': 'sprite', '원가': 1450, '정가': 1800, '수량': 5, '무게': 15},
         5: {'이름': 'zerosprite', '원가': 1350, '정가': 1800, '수량': 5, '무게': 15},
         6: {'이름': 'chilsungCider', '원가': 1600, '정가': 2100, '수량': 5, '무게': 15},
         7: {'이름': 'chilsungCiderZero', '원가': 1600, '정가': 2100, '수량': 5, '무게': 15},
         8: {'이름': 'Milkis', '원가': 1300, '정가': 1600, '수량': 6, '무게': 12},
         9: {'이름': 'Isis', '원가': 500, '정가': 850, '수량': 8, '무게': 8},
         10: {'이름': 'samdasu', '원가': 500, '정가': 900, '수량': 8, '무게': 8},
         11: {'이름': 'pocarisweat', '원가': 1600, '정가': 2200, '수량': 4, '무게': 18},
         12: {'이름': 'evian', '원가': 900, '정가': 1100, '수량': 8, '무게': 8},
         13: {'이름': 'lemongreentea', '원가': 500, '정가': 900, '수량': 9, '무게': 6},
         14: {'이름': 'gatorade', '원가': 1500, '정가': 2000, '수량': 4, '무게': 19},
         15: {'이름': 'fantaorange', '원가': 1100, '정가': 1500, '수량': 8, '무게': 9},
         16: {'이름': 'fantagrape', '원가': 1100, '정가': 1500, '수량': 8, '무게': 9},
         17: {'이름': 'demisodaapple', '원가': 400, '정가': 800, '수량': 9, '무게': 7},
         18: {'이름': 'seagram', '원가': 1000, '정가': 1500, '수량': 9, '무게': 6},
         19: {'이름': 'welchs', '원가': 900, '정가': 1200, '수량': 9, '무게': 9},
         20: {'이름': 'letsbe', '원가': 400, '정가': 700, '수량': 9, '무게': 6} }
# 제품 class 선언하기
class Product:
    def __init__(self,name,cost,price,quantity,weight):
        self.name = name
        self.cost = cost                       # 원가
        self.price = price                     # 정가
        self.revenue = price - cost            # 순이익 = 정가 - 원가
        self.quantity = quantity               # 수량
        self.weight = weight                   # 무게

# 추천시스템 class 구현하기
class recommendation(object):
    def __init__(self, juice, amount):
        self.juice = juice                  #이중 딕셔너리로 되어있는 품목들 저장하기
        self.Itemset = []                   #품목을 class로 변환시킨후 저장
        self.total_revenue = 0
        self.max_weight = 500               #최대무게하중
        self.result = []                    #추천시스템 실행 시 최종 결과
        self.amount = amount                #자판기에 넣을 음료의 개수

        for key, value in juice.items():    #juice 딕셔너리를 class로 변환하기
            item = Product(value['이름'], value['원가'], value['정가'], value['수량'], value['무게'])
            self.Itemset.append(item)

    def print_All_Items(self):              #모든 아이템 목록 출력
        print("     ",'%-18s' % "product", '%-6s' % "cost", '%-6s' % "price", '%-9s' % "quantity", '%-3s' % "weight")
        index = 0
        for item in self.Itemset:
            if item == None :
                print('%-3s' % index)
            elif item == 0 :
                print('%-3s' % index)
            else:
                print('%-3s' % index,' ','%-18s'% item.name,'%-6s'% item.cost,'%-6s'% item.price,'  ','%-7s'% item.quantity,'%-3s'% item.weight)
            index +=1
        print()

    def Findcase(self):                     #brute force로 최적해 찾기
        self.total_revenue = 0
        item_count = len(self.Itemset)
        case_count = 2 ** item_count - 1
        for case in range(1, case_count + 1):
            revenue = 0
            weight = 0
            num = 0
            output = []
            for bitnum in range(item_count):
                target_bit_num = 2 ** bitnum
                if (case & target_bit_num == target_bit_num):
                    item = self.Itemset[bitnum]
                    revenue += (item.revenue*item.quantity)
                    weight += (item.weight*item.quantity)
                    num += 1
                    output.append(item)
            if num <= self.amount:
                if (revenue > self.total_revenue and weight <= self.max_weight):
                    self.opt_case = case
                    self.total_revenue = revenue
                    self.total_weight = weight
                    self.result = output
                chosen_items = self.decodeCase(self.opt_case)
        return (chosen_items, self.total_revenue, self.total_weight)

    def decodeCase(self, case):
        item_count = len(self.Itemset)
        chosen_items = []

        for index in range(item_count):
            target_bit_num = 2 ** index
            if (case & target_bit_num == target_bit_num):
                item = self.Itemset[index]
                chosen_items.append(item.name)
        return chosen_items

# 자판기 class 구현하기
class Vendingmachine:
    def __init__(self,size):
        self.tablesize = size                  # 자판기 사이즈를 저장한다
        self.table = [None]*size               # 자판기 사이즈에 맞는 배열을 생성한다

        self.user_money = 0                    # 사용자가 넣은 돈
        self.user_choice = {}                  # 사용자가 장바구니에 넣은 물건 정보
        self.user_total_price = 0              # 사용자가 장바구니에 넣은 물건의 총 금액
        self.basket_revenue = 0

        self.total_revenue = 0                 # 자판기의 매출액
        self.net_income = 0                    # 자판기의 순이익

        self.max_weight = 500                  # 자판기 최대 하중

    def convert_ascii(self,name):              # key값을 아이템 이름으로 하기위해서 아이템이름을 ascii코드로 바꾸는 코드를 구현한다
        ascii_num = 0
        for character in name:
            ascii_num+=ord(character)
        return ascii_num

    def hash(self,key):                        # ascii코드로 바꾼 값을 hash함수를 통해 변환하는 과정이다
        return key % self.tablesize

    def add(self,name,cost,price,quantity,weight):
        product = Product(name,cost,price,quantity,weight)
        key = self.convert_ascii(product.name)
        initial_position = self.hash(key)
        position = initial_position
        boolean = True
        while boolean:
            fproduct = self.table[position]
            if(fproduct == None):
                self.table[position]= product
                break
            if (fproduct == 0):
                self.table[position] = product
                break
            elif(self.convert_ascii(fproduct.name) == key):
                self.table[position]= product
                break
            position = (position+1)%self.tablesize
            if position == initial_position:
                print('품목이 다 차있습니다')
                boolean = False

    # 품목을 정해진 수량만큼 빼기
    def subtract(self,name,quantity):
        key = self.convert_ascii(name)
        initial_position = self.hash(key)
        position = initial_position
        while True :
            fproduct = self.table[position]
            if(fproduct == None):
                return print('빼려는 품목이 없습니다')
            elif(self.convert_ascii(fproduct.name) == key):
                break
            position = (position+1)%self.tablesize
            if position == initial_position:
                return print('빼려는 품목이 없습니다')
            break
        num = fproduct.quantity - quantity
        if (num < 0):
            return print('빼려는 수량이 기존 수량보다 많습니다.')
        elif (num == 0):
            self.table[position] = 0
            print('품목이 완전히 삭제되었습니다.')
            return
        else :
            fproduct.quantity = fproduct.quantity - quantity

    #모든 아이템 목록 출력
    def print_product_administer(self):
        print("     ",'%-18s' % "product", '%-6s' % "cost", '%-6s' % "price", '%-9s' % "quantity", '%-3s' % "weight")
        index = 0
        for item in self.table:
            if item == None :
                print('%-3s' % index)
            elif item == 0 :
                print('%-3s' % index)
            else:
                print('%-3s' % index,' ','%-18s'% item.name,'%-6s'% item.cost,'%-6s'% item.price,'  ','%-7s'% item.quantity,'%-3s'% item.weight)
            index +=1
        print()

    def print_product(self):
        print("     ",'%-18s' % "product", '%-6s' % "price", '%-9s' % "quantity")
        index = 0
        for product in self.table:
            if product == None:
                print('%-3s' % index)
            elif product == 0:
                print('%-3s' % index)
            else:
                print('%-3s' % index, ' ', '%-18s' % product.name, '%-6s' % product.price, '  ',
                      '%-7s' % product.quantity)
            index += 1
        print()

    # =================================================================================================================
    # 1차 화면: 관리자 메뉴 or <구매 하기>
    def start_menu(self):
        print("---------------------------------------------------")
        print("1. 관리자 메뉴\n2. 구매하기")
        while True:
            user_select = input(">> 번호를 입력하세요: ")
            if user_select == '1':
                print("---------------------------------------------------")
                self.administer()
                break
            elif user_select == '2':
                print("---------------------------------------------------")
                self.buy_menu()
                break
            else:
                print("번호를 다시 입력해주세요")
    # =================================================================================================================
    # 2차 화면 : <관리자 메뉴> 구현하기
    def administer(self):
        print("총 매출액: ",self.total_revenue, "총 순이익: ", self.net_income)
        print("  <관리자 메뉴>\n1. 현재품목 확인하기\n2. 제품 추가\n3. 제품 제거\n4. 추천 시스템 사용하기\n5. 처음으로 가기")
        while True:
            user_select = input(">> 번호를 입력하세요: ")
            if user_select == '1':
                print("---------------------------------------------------")
                self.print_product_administer()
                print('관리자 메뉴로 돌아가려면 1를 입력하세요')
                num = input(">> 번호를 입력하세요 ")
                if num == '1':
                    print("---------------------------------------------------")
                    self.administer()
                break
            elif user_select == '2':
                print("---------------------------------------------------")
                while(True):
                    name,cost,price,quantity,weight = self.input()
                    print('입력한 값이 맞습니까? yes:1, no:2\n')
                    num = input(">> 번호를 입력하세요 ")
                    if num == '1':
                        cost = int(cost)
                        price = int(price)
                        quantity = int(quantity)
                        weight = int(weight)
                        self.add(name,cost,price,quantity,weight)
                        print('제품을 성공적으로 추가했습니다')
                        print("---------------------------------------------------")
                        self.administer()
                    if num == '2':
                        print('관리자 메뉴로 돌아가겠습니다')
                        print("---------------------------------------------------")
                        self.administer()
                    else:
                        break
            elif user_select == '3':
                print("---------------------------------------------------")
                while(True):
                    name = input(">> 빼려는 품목을 입력하세요 : ")
                    quantity = int(input(">> 빼려는 수량을 입력하세요 : "))
                    print()
                    print(name+'를 '+str(quantity)+'개 빼겠습니다, 입력한 값이 맞습니까? yes:1, no:2')
                    num = input(">> 번호를 입력하세요 ")
                    if num == '1':
                        self.subtract(name,quantity)
                        print("---------------------------------------------------")
                        self.administer()
                    if num == '2':
                        print('관리자 메뉴로 돌아가겠습니다')
                        print("---------------------------------------------------")
                        self.administer()
                    break

            if user_select == '4':
                while True:
                    print("---------------------------------------------------")
                    print("추천시스템을 사용하시겠습니까?\n1. 예\n2. 아니오\n3. 전체 리스트 보기")
                    user_select = input(">> 번호를 입력하세요: ")
                    a = recommendation(juice, 7)
                    if user_select == '1':
                        self.table = [None]*self.tablesize
                        print('추천시스템 사용 결과: ', a.Findcase())         #추천시스템 실행
                        for item in a.result:                                #결과 자판기에 넣기
                            self.add(item.name,item.cost,item.price,item.quantity,item.weight)
                        print('추천된 품목을 자판기에 넣겠습니다')
                        print("관리자 메뉴로 돌아가겠습니다")
                        print("---------------------------------------------------")
                        self.administer()
                        break

                    if user_select == '2':
                        print("관리자 메뉴로 돌아가겠습니다")
                        print("---------------------------------------------------")
                        self.administer()
                        break
                    if user_select == '3':
                        a.print_All_Items()
                    else:
                        print("번호를 다시 입력해주세요")
            elif user_select == '5':
                self.start_menu()
                break
            else:
                print("번호를 다시 입력해주세요")
            break

    # <관리자 메뉴>에서 2번 제품추가 함수 선언하기
    def input(self):
        print('제품정보를 입력하세요 이름,원가,정가,수량,무게 순으로 입력해주세요')
        name = input(">> name : ")
        cost = (input(">> cost : "))
        price = (input(">> price : "))
        quantity = (input(">> quantity : "))
        weight = (input(">> weight : "))
        print()
        print('입력한 값은 ',name,'원가 :',cost,'정가 :',price,'수량 :',quantity,'무게 :',weight,'입니다\n')
        return name,cost,price,quantity,weight


    # =================================================================================================================
    # 2차 화면: <구매 하기> 선택시 ----- <현금 투입> <물건 구입> 버튼과 잔액출력
    def buy_menu(self):
        print("현재 투입 금액:",self.user_money)
        print("1. 현금 투입\n2. 물건 구입\n3. 종료")
        while True:
            user_select = input(">> 번호를 입력하세요: ")
            if user_select == '1':
                print("---------------------------------------------------")
                self.set_money()
                break
            elif user_select == '2':
                print("---------------------------------------------------")
                self.select_product()
                break
            elif user_select == '3':     # 종료 및 잔액 반환
                print("잔액을 반환 후 종료합니다")
                print("반환 금액:",self.user_money)
                print("종료되었습니다.")
                print("---------------------------------------------------")
                self.user_money = 0
                break
            else:
                print("번호를 다시 입력해주세요")

    # =======================================================================================================
    # 3차 화면: <현금 투입> ----- 1. 금액 입력 2. 투입 종료 + 현재 금액 실시간 산출
    def set_money(self):
        while True:
            print("현재 투입 금액:", self.user_money)
            user_input = input(">> 금액을 입력하세요 (뒤로 가려면 0을 입력하세요): ")
            if (user_input == '0'):
                print("---------------------------------------------------")
                self.buy_menu()
                break
            else:
                input_money = int(user_input)
                self.user_money += input_money
                print("---------------------------------------------------")


    # 물건 선택 화면: 상품을 입력하면 입력받는 역할

    # 0을 입력할 때 종료 & 결과값 프린트 (반복문을 돌려서 딕셔너리 안의 값들을 합하여 장바구니 상품의 총 value값 합 산출)
    # check_price() 통해 구매 가능 여부 판별

    # 물건이 없을 때 없다고 출력

    # 사용자의 장바구니에 넣는 역할(이중 딕셔너리를 이용해 상품별 수량, 총 금액, 순이익 저장)

    def select_product(self):
        self.print_product()
        print("현재 투입 금액:", self.user_money)

        while True:
            input_product = input("구매하려는 상품명 입력 (전부 골랐다면 0을 입력):")

            if (input_product == "0"):
                print("---------------------------------------------------")
                self.user_total_price = 0
                print("\n<장바구니에 담긴 품목>")
                print('%-8s' % "물품", '%-5s' % "수량")
                for item in self.user_choice:
                    basket = self.user_choice[item]
                    self.user_total_price += basket['sum_price']
                    self.basket_revenue += basket['sum_revenue']
                    name = item
                    quantity = basket['qty']
                    print('%-10s' % name,'%-5s' % quantity)
                print()
                print('%-8s' % "총 물품 금액:", self.user_total_price, "원")
                print('%-8s' % "현재 투입 금액:", self.user_money, "원\n")
                self.check_price()
                break

            if (self.search_in(input_product) == None):
                print("찾으시는 물건이 없습니다. 다시 입력하십시오.\n")
                continue
            else:
                select_obj = self.search_in(input_product)
                item_name = select_obj.name
                if item_name in self.user_choice:
                    change_item_value = self.user_choice[item_name]
                    if ((change_item_value['qty'] + 1) > select_obj.quantity):
                        print("자판기에 상품이 다 떨어졌습니다.\n")
                    else:
                        change_item_value['qty'] += 1
                        change_item_value['sum_price'] = select_obj.price * change_item_value['qty']
                        change_item_value['sum_revenue'] = select_obj.revenue * change_item_value['qty']
                        print("장바구니에", item_name, "이(가)", change_item_value['qty'], "개가 되었습니다\n")
                else:
                    self.user_choice[item_name] = {'qty': 1, 'sum_price': select_obj.price, 'sum_revenue': select_obj.revenue}
                    print("장바구니에",item_name,"이(가) 담겼습니다\n")

    def search_in(self,item):
        key = self.convert_ascii(item)
        initial_position = self.hash(key)
        position = initial_position

        while True:
            fproduct = self.table[position]
            if (fproduct != 0):
                if (fproduct == None):
                    return None

                if fproduct.name == item:
                    return fproduct

            position = (position + 1) % self.tablesize
            if position == initial_position:
                return None

    # 구매를 진행할 경우 자판기의 품목별 수량을 반영해준다.

    def reflect_quantity(self):
        for item in self.user_choice:
            basket = self.user_choice[item]
            quantity = basket['qty']

            key = self.convert_ascii(item)
            initial_position = self.hash(key)
            position = initial_position

            while True:
                fproduct = self.table[position]
                if (self.convert_ascii(fproduct.name) == key):
                    break
                position = (position + 1) % self.tablesize

            num = fproduct.quantity - quantity
            if (num == 0):
                self.table[position] = 0
            else:
                fproduct.quantity = num

    # 1. 구매 가능 금액일 경우 -> 구매 하고 품목 수량 감소 (reflect_quantity) & 자판기 총 수입량 반영 ()
    # 2. 구매 불가 금액일 경우 (첫번째 or 두번째 선택 후 반복)
    # 첫번째: 금액 추가 입력
    # 두번째: 물건 다시 선택

    def check_price(self):
        if (self.user_total_price <= self.user_money):
            self.user_money -= self.user_total_price
            self.total_revenue += self.user_total_price
            self.net_income += self.basket_revenue

            self.reflect_quantity()

            print("구매가 완료되었습니다",self.user_total_price,"원 결제 완료")
            print("잔액을 반환 후 종료합니다")
            print("반환 금액:", self.user_money)
            print("종료되었습니다.")
            print("---------------------------------------------------")

            self.user_money = 0
            self.user_total_price = 0
            self.basket_revenue = 0
            self.user_choice = {}
            return

        else:
            print("구매하실 수 없습니다.")
            print("1. 현금을 더 넣습니다.\n2. 물건을 다시 선택합니다.\n3. 종료합니다.\n")

            while True:
                user_select = input(">> 번호를 입력하세요: ")
                if user_select == '1':
                    print("---------------------------------------------------")
                    while True:
                        print("현재 투입 금액:", self.user_money)
                        print("현재 물품 금액:", self.user_total_price)
                        user_input = input(">> 금액을 입력하세요 (뒤로 가려면 0을 입력하세요): ")
                        if (user_input == '0'):
                            print("---------------------------------------------------")
                            self.check_price()
                            break
                        else:
                            input_money = int(user_input)
                            self.user_money += input_money
                            print("---------------------------------------------------")
                            self.check_price()
                            break
                    break
                elif user_select == '2':
                    print("---------------------------------------------------")
                    print("물건을 다시 선택합니다.")
                    self.user_total_price = 0
                    self.basket_revenue = 0
                    self.user_choice = {}
                    self.select_product()
                    break
                elif user_select == '3':
                    print("잔액을 반환 후 종료합니다")
                    print("반환 금액:", self.user_money)
                    print("종료되었습니다.")
                    print("---------------------------------------------------")
                    self.user_money = 0
                    self.user_total_price = 0
                    self.basket_revenue = 0
                    self.user_choice = {}
                    return
                else:
                    print("번호를 다시 입력해주세요")

t = Vendingmachine(7)

while True:
    t.print_product_administer()
    t.start_menu()
    input()