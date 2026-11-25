
# מחלקה המייצגת גוף פיזיקלי
class Body:

        # אתחול תכונות הגוף ובדיקת תקינות הערכים
    def __init__(self, mass, heat_capacity, temperature):

        if mass > 0:
            self.mass = mass
        else:
            self.mass = 0.01

        if heat_capacity > 0:
            self.heat_capacity = heat_capacity
        else:
            self.heat_capacity = 0.01

        if temperature >= 0:
            self.temperature = temperature
        else:
            self.temperature = 0

    # הוספת או הוצאת חום מהגוף
    def add_heat(self, heat):
        delta_temperature = heat / (self.mass * self.heat_capacity) # חישוב השינוי בטמפרטורה
        self.temperature += delta_temperature # עדכון הטמפרטורה של הגוף
        return self.temperature # החזרת הטמפרטורה החדשה של הגוף

# בדיקת המחלקה בהרצה ישירה של הקובץ
if __name__ == "__main__":
    # יצירת גוף פיזיקלי עם נתונים התחלתיים
    body = Body(100, 0.15, 200)

    # הצגת הטמפרטורה ההתחלתית
    print("Initial temperature:", body.temperature)

    # הוספת 20 ג'אול לגוף
    print("Temperature after adding heat:", body.add_heat(20))

    # הוצאת 40 ג'אול מהגוף
    print("Temperature after removing heat:", body.add_heat(-40))