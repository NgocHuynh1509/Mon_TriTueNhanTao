#Tên: Huỳnh Gia Diễm Ngọc
#MSSV: 23110132
#Bài tập về nhà tuần 1: Hệ chuyên gia

class tri_thuc:
    def __init__(self):
        self.he_tri_thuc = {
            "1":{
            "hỏi":"Bạn muốn ăn đồ nước(1) hay đồ khô(2)? (Nhập 1/2)",
            "2":"khô",
            "1":"nước"
            },
            "2":{
            "hỏi":"Bạn muốn ăn chè(1) hay uống trà sữa(2)",
            "1":"chè",
            "2":"trà sữa",
            },
            "chè":{
            "trả lời":"Chè bơ đi bạn, chè bơ làng đh siu ngon!!!"
            },
            "trà sữa":{
            "trả lời":"Trà sữa bé nò làng đh nhìu topping lắm!!"
            },
            "khô":{
            "hỏi": "Bạn ăn bò(1), gà(2), heo(3)",
            "1":"bò", "2":"gà", "3":"heo"
            },
            "bò":{
            "trả lời":"Bún bò nướng Mai Thu Kiều -.-"
            },
            "gà":{
            "trả lời":"Cơm gà Bùi Lộc"
            },
            "heo":{
            "trả lời":"Bánh cuốn heo quay căn teen D5"
            },
            "nước":{
            "hỏi": "Bạn ăn bò(1) hay cá(2)",
            "1":"bò nước", "2":"cá"
            },
            "bò nước":{
            "trả lời":"Bún bò nhen. Đại đại đi chỗ náo cũng được"
            },
            "cá":{
            "trả lời":"Bánh canh hẹ Phú Yên ik bn. Ăn thử cho biết"
            },
            
        }

    

    def bo_xu_ly(self, problem):
        node = self.he_tri_thuc[problem]
        if "hỏi" in node:
            print(node["hỏi"])
            answer = input("705: ").lower()
            if answer in node:
                self.bo_xu_ly(node[answer])
            elif answer in self.he_tri_thuc:   
                self.bo_xu_ly(answer)
            else:
                print("Làm gì có lựa chọn đó mà chọn")
        elif "trả lời" in node:
            print(node["trả lời"])

    def start(self):
            print("Hôm nay C5 - 705 tối nay ăn gì")
            choice = input("Phòng mình mún ăn đồ ăn tối (1) hay tráng miệng (2) ak\n705 (Nhập 1/2): ",).lower()
            if choice in self.he_tri_thuc:
                self.bo_xu_ly(choice)
            else:
                print("Phòng mình nay có vẻ không đói, thoi khỏi ăn vậy")

if __name__ == '__main__':
    exp = tri_thuc()
    exp.start()
