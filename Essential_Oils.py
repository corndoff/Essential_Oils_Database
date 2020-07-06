import kivy
from kivy.app import App
from kivy.lang  import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3

conn = sqlite3.connect('mom.db')
c = conn.cursor()

def add_table():
        c.execute('CREATE TABLE IF NOT EXISTS oil(name TEXT, amount INTEGER)')

class MainWindow(Screen):
    pass
        
class SecondWindow(Screen):
    oilName = ObjectProperty(None)
    oilAmt = ObjectProperty(None)
    
    def reset(self):
        self.oilName.text = ""
        self.oilAmt.text = ""
        
    def add_oil(self):
        c.execute("INSERT INTO oil(name, amount) VALUES(?, ?)", (self.oilName.text, self.oilAmt.text))
        conn.commit()
        
class ThirdWindow(Screen):
    tryingthis = ObjectProperty(None)
    
    
    def get_names(self):
        c.execute("SELECT * FROM oil")
        names = c.fetchall()
        for n in names:
            self.ids.tryingthis.text = n[0]
        
class FourthWindow(Screen):
    oilName= ObjectProperty(None)
    addAmt= ObjectProperty(None)
    subAmt= ObjectProperty(None)
    oldAmt= ObjectProperty(None)
    newAmt= ObjectProperty(None)
    
    def reset(self):
        self.oilName.text = ""
        self.addAmt.text = ""
        self.subAmt.text = ""
        
        
    def add_to_oil(self):
        c.execute("SELECT amount FROM oil WHERE name =?", (self.oilName.text, ))
        oldAddAmt = c.fetchone()[0]
        
        addedAmt = int(self.addAmt.text)
        newAmt = oldAddAmt + addedAmt
        
        c.execute("UPDATE oil SET amount=? WHERE name=?", (newAmt, self.oilName.text))
        conn.commit()

    def sub_from_oil(self):
        c.execute("SELECT amount FROM oil WHERE name = ?", (self.oilName.text, ))
        oldSubAmt = c.fetchone()[0]
        
        subedAmt = int(self.subAmt.text)
        newSubAmt = oldSubAmt - subedAmt
        
        c.execute("UPDATE oil SET amount=? WHERE name=?", (newSubAmt, self.oilName.text))
        conn.commit()

class FifthWindow(Screen):
    removeOil= ObjectProperty(None)

    def reset(self):
        self.removeOil.text = ""

    def remove_oil(self):
        c.execute("DELETE FROM oil WHERE name = ?", (self.removeOil.text,))
        conn.commit()
                  
class WindowManager(ScreenManager):
    pass



add_table()

kv = Builder.load_file("mom2.kv")
class MyApp(App):
    def build(self):
        return kv
        c.close()
        conn.close()

if __name__=="__main__":
    MyApp().run()
