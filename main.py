import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import sqlite3


class AnaEkran(Screen):
    def tohesaplama(self):
        app.root.current = "hesaplama"
    def toayarlar(self):
        app.root.current = "ayarlar"


class Hesaplama(Screen):
    planebem = 0
    planearm = 0
    sparm = 0
    fiarm = 0
    rs1arm = 0
    rs2arm = 0
    ba1arm = 0
    ba2arm = 0
    fuelarm = 0
    fiweight = 0

    spinnerucak = ObjectProperty()
    spinnerfi = ObjectProperty()

    def spinnerfihesapla(self):
        adsoyad = self.ids.spinnerfi.text
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("Select * From fiinfo where adsoyad = ?", (adsoyad,))
        fiinfo = cursor.fetchall()
        self.fiweight = fiinfo[0][1]
        self.ids.fi_weight_label.text = str(self.fiweight)

    def spinnerucakhesapla(self):
        registration = self.ids.spinnerucak.text
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("Select * From ucaklar where registration = ?", (registration,))
        aircraftinfo = cursor.fetchall()
        self.planebem = aircraftinfo[0][1]
        self.planearm = aircraftinfo[0][2]
        self.sparm = aircraftinfo[0][3]
        self.fiarm = aircraftinfo[0][4]
        self.rs1arm = aircraftinfo[0][5]
        self.rs2arm = aircraftinfo[0][6]
        self.ba1arm = aircraftinfo[0][7]
        self.ba2arm = aircraftinfo[0][8]
        self.fuelarm = aircraftinfo[0][9]
        self.ids.bem_label.text = str(self.planebem)
        self.ids.plane_arm_label.text = str(self.planearm)
        self.ids.sp_arm_label.text = str(self.sparm)
        self.ids.fi_arm_label.text = str(self.fiarm)
        self.ids.rs1_arm_label.text = str(self.rs1arm)
        self.ids.rs2_arm_label.text = str(self.rs2arm)
        self.ids.ba1_arm_label.text = str(self.ba1arm)
        self.ids.ba2_arm_label.text = str(self.ba2arm)
        self.ids.fuel_arm_label.text = str(self.fuelarm)

    def hesapla(self):
        if (self.ids.sp_input.text) == "":
            sp_weight = 0
        else:
            sp_weight = float(self.ids.sp_input.text)

        if (self.ids.rs1_input.text) == "":
            rs1_weight = 0
        else:
            rs1_weight = float(self.ids.rs1_input.text)
        if (self.ids.rs2_input.text) == "":
            rs2_weight = 0
        else:
            rs2_weight = float(self.ids.rs2_input.text)
        if (self.ids.ba1_input.text) == "":
            ba1_weight = 0
        else:
            ba1_weight = float(self.ids.ba1_input.text)
        if (self.ids.ba2_input.text) == "":
            ba2_weight = 0
        else:
            ba2_weight = float(self.ids.ba2_input.text)
        if (self.ids.fuel_input.text) == "":
            fuel = 0
        else:
            fuel = float(self.ids.fuel_input.text)
        fuelweight = fuel * 6

        plane_moment = self.planebem * self.planearm
        self.ids.plane_moment_label.text = "{:.1f}".format(plane_moment)
        sp_moment = sp_weight * self.sparm
        self.ids.sp_moment_label.text = "{:.1f}".format(sp_moment)
        fi_moment = self.fiweight * self.fiarm
        self.ids.fi_moment_label.text = "{:.1f}".format(fi_moment)
        rs1_moment = rs1_weight * self.rs1arm
        self.ids.rs1_moment_label.text = "{:.1f}".format(rs1_moment)
        rs2_moment = rs2_weight * self.rs2arm
        self.ids.rs2_moment_label.text = "{:.1f}".format(rs2_moment)
        ba1_moment = ba1_weight * self.ba1arm
        self.ids.ba1_moment_label.text = "{:.1f}".format(ba1_moment)
        ba2_moment = ba2_weight * self.ba2arm
        self.ids.ba2_moment_label.text = "{:.1f}".format(ba2_moment)
        fuel_moment = fuelweight * self.fuelarm
        self.ids.fuel_moment_label.text = "{:.1f}".format(fuel_moment)

        totalweight = self.planebem + sp_weight + self.fiweight + rs1_weight + rs2_weight + ba1_weight + ba2_weight + fuelweight
        self.ids.total_weight_label.text = "{:.1f}".format(totalweight)
        totalmoment = plane_moment + sp_moment + fi_moment + rs1_moment + rs2_moment + ba2_moment + ba2_moment + fuel_moment
        self.ids.total_moment_label.text = "{:.1f}".format(totalmoment)
        try:
            self.ids.cog_label.text = "{:.2f}".format(totalmoment / totalweight)
            if totalmoment / totalweight == 0:
                raise ZeroDivisionError
        except ZeroDivisionError:
            self.ids.cog_label.text = "0"

    def toayarlar(self):
        app.root.current = "ayarlar"


class Ayarlar(Screen):
    def toucakayarlar(self):
        app.root.current = "ucakayarlar"
    def tofiayarlar(self):
        app.root.current = "fiayarlar"
    def toanaekran(self):
        app.root.current = "anaekran"


class UcakAyarlar(Screen):
    def toucakekle(self):
        app.root.current = "ucakekle"
    def toucakeupdate(self):
        app.root.current = "ucakupdate"
    def toucaksil(self):
        app.root.current = "ucaksil"
    def toayarlar(self):
        app.root.current = "ayarlar"


class UcakEkle(Screen):

    def ekletodb(self):
        if self.ids.registration_input_ekle.text in app.values:
            app.warn = "Aircraft already exists."
            self.ids.registration_input_ekle.text = ""
            self.ids.bem_input_ekle.text = ""
            self.ids.planearm_input_ekle.text = ""
            self.ids.sparm_input_ekle.text = ""
            self.ids.fiarm_input_ekle.text = ""
            self.ids.rs1arm_input_ekle.text = ""
            self.ids.rs2arm_input_ekle.text = ""
            self.ids.ba1arm_input_ekle.text = ""
            self.ids.ba2arm_input_ekle.text = ""
            self.ids.fuelarm_input_ekle.text = ""
            app.warn = "Aircraft already exists"
            show_popup()
            app.root.current = "ucakekle"
        else:
            con = sqlite3.connect("database.db")
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO ucaklar (registration, bem, planearm, sparm, fiarm, rs1arm, rs2arm, b1arm, b2arm, fuelarm) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (self.ids.registration_input_ekle.text, self.ids.bem_input_ekle.text, self.ids.planearm_input_ekle.text, self.ids.sparm_input_ekle.text,
                 self.ids.fiarm_input_ekle.text, self.ids.rs1arm_input_ekle.text, self.ids.rs2arm_input_ekle.text, self.ids.ba1arm_input_ekle.text,
                 self.ids.ba2arm_input_ekle.text, self.ids.fuelarm_input_ekle.text))
            con.commit()
            con.close()

            con = sqlite3.connect("database.db")
            cursor = con.cursor()
            cursor.execute("Select registration From ucaklar")
            new_data = [r[0] for r in cursor.fetchall()]
            app.values = new_data

            self.ids.registration_input_ekle.text = ""
            self.ids.bem_input_ekle.text = ""
            self.ids.planearm_input_ekle.text = ""
            self.ids.sparm_input_ekle.text = ""
            self.ids.fiarm_input_ekle.text = ""
            self.ids.rs1arm_input_ekle.text = ""
            self.ids.rs2arm_input_ekle.text = ""
            self.ids.ba1arm_input_ekle.text = ""
            self.ids.ba2arm_input_ekle.text = ""
            self.ids.fuelarm_input_ekle.text = ""

            app.warn = "Aircraft has been added to Database succesfully."
            show_popup()

            app.root.current = "anaekran"

    def toucakayarlar(self):
        self.ids.registration_input_ekle.text = ""
        self.ids.bem_input_ekle.text = ""
        self.ids.planearm_input_ekle.text = ""
        self.ids.sparm_input_ekle.text = ""
        self.ids.fiarm_input_ekle.text = ""
        self.ids.rs1arm_input_ekle.text = ""
        self.ids.rs2arm_input_ekle.text = ""
        self.ids.ba1arm_input_ekle.text = ""
        self.ids.ba2arm_input_ekle.text = ""
        self.ids.fuelarm_input_ekle.text = ""
        app.root.current = "ucakayarlar"


class UcakUpdate(Screen):
    spinnerupdate = ObjectProperty()

    def filltextinputs(self):
        registration = self.ids.spinnerupdate.text
        if registration == "Choose":
            self.ids.registration_input_update.text = ""
            self.ids.bem_input_update.text = ""
            self.ids.planearm_input_update.text = ""
            self.ids.sparm_input_update.text = ""
            self.ids.fiarm_input_update.text = ""
            self.ids.rs1arm_input_update.text = ""
            self.ids.rs2arm_input_update.text = ""
            self.ids.ba1arm_input_update.text = ""
            self.ids.ba2arm_input_update.text = ""
            self.ids.fuelarm_input_update.text = ""

        else:
            con = sqlite3.connect("database.db")
            cursor = con.cursor()
            cursor.execute("Select * From ucaklar where registration = ?", (registration,))
            aircraftinfo2 = cursor.fetchall()
            reg = aircraftinfo2[0][0]
            bem2 = aircraftinfo2[0][1]
            planearm2 = aircraftinfo2[0][2]
            sparm2 = aircraftinfo2[0][3]
            fiarm2 = aircraftinfo2[0][4]
            rs1arm2 = aircraftinfo2[0][5]
            rs2arm2 = aircraftinfo2[0][6]
            ba1arm2 = aircraftinfo2[0][7]
            ba2arm2 = aircraftinfo2[0][8]
            fuelarm2 = aircraftinfo2[0][9]
            self.ids.registration_input_update.text = str(reg)
            self.ids.bem_input_update.text = str(bem2)
            self.ids.planearm_input_update.text = str(planearm2)
            self.ids.sparm_input_update.text = str(sparm2)
            self.ids.fiarm_input_update.text = str(fiarm2)
            self.ids.rs1arm_input_update.text = str(rs1arm2)
            self.ids.rs2arm_input_update.text = str(rs2arm2)
            self.ids.ba1arm_input_update.text = str(ba1arm2)
            self.ids.ba2arm_input_update.text = str(ba2arm2)
            self.ids.fuelarm_input_update.text = str(fuelarm2)


    def updatetodb(self):
        registration5 = self.ids.spinnerupdate.text
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute(
            "UPDATE ucaklar SET registration = ?, bem = ?, planearm = ?, sparm = ?, fiarm = ?, rs1arm = ?, rs2arm = ?, b1arm = ?, b2arm = ?, fuelarm  = ? where registration = ?",
            (self.ids.registration_input_update.text, self.ids.bem_input_update.text, self.ids.planearm_input_update.text, self.ids.sparm_input_update.text,
             self.ids.fiarm_input_update.text, self.ids.rs1arm_input_update.text, self.ids.rs2arm_input_update.text, self.ids.ba1arm_input_update.text,
             self.ids.ba2arm_input_update.text, self.ids.fuelarm_input_update.text, registration5))
        con.commit()
        con.close()

        self.ids.registration_input_update.text = ""
        self.ids.bem_input_update.text = ""
        self.ids.planearm_input_update.text = ""
        self.ids.sparm_input_update.text = ""
        self.ids.fiarm_input_update.text = ""
        self.ids.rs1arm_input_update.text = ""
        self.ids.rs2arm_input_update.text = ""
        self.ids.ba1arm_input_update.text = ""
        self.ids.ba2arm_input_update.text = ""
        self.ids.fuelarm_input_update.text = ""


        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("Select registration From ucaklar")
        new_data = [r[0] for r in cursor.fetchall()]
        app.values = new_data
        self.ids.spinnerupdate.text = "Choose"

        app.warn = "Update successful"
        show_popup()

        app.root.current = "anaekran"

    def toucakayarlar(self):
        self.ids.spinnerupdate.text = "Choose"
        app.root.current = "ucakayarlar"


class UcakSil(Screen):
    spinnerdelete = ObjectProperty()

    def filltextinputs(self):
        registrationdelete = self.ids.spinnerdelete.text
        if registrationdelete == "Choose":
            self.ids.delete_label.text = ""
            self.ids.delete_aircraft_label.text = ""
        else:
            self.ids.delete_label.text = "Delete   "
            self.ids.delete_aircraft_label.text = str(registrationdelete) + "  ?"

    def deletefromdb(self):
        registration6 = self.ids.spinnerdelete.text
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("Delete from ucaklar where registration = ? ", (registration6,))
        con.commit()
        con.close()

        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("Select registration From ucaklar")
        new_data = [r[0] for r in cursor.fetchall()]
        app.values = new_data

        self.ids.spinnerdelete.text = "Choose"

        app.warn = "Aircraft deleted"
        show_popup()

        app.root.current = "anaekran"

    def toucakayarlar(self):
        self.ids.spinnerdelete.text = "Choose"
        app.root.current = "ucakayarlar"



class FiAyarlar(Screen):
    def tofiekle(self):
        app.root.current = "fiekle"

    def tofiupdate(self):
        app.root.current = "fiupdate"

    def tofisil(self):
        app.root.current = "fisil"

    def toayarlar(self):
        app.root.current = "ayarlar"


class FiEkle(Screen):
    def fiekletodb(self):
        if self.ids.fullname_input_ekle.text in app.valuesfi:
            self.ids.fullname_input_ekle.text = ""
            self.ids.fiweight_input_ekle.text = ""

            app.warn = "FI/Co-Pilot already exists"
            show_popup()

            app.root.current = "fiekle"
        else:
            con = sqlite3.connect("database.db")
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO fiinfo (adsoyad, fiweight) VALUES (?,?)",
                (self.ids.fullname_input_ekle.text, self.ids.fiweight_input_ekle.text))
            con.commit()
            con.close()

            con = sqlite3.connect("database.db")
            cursor = con.cursor()
            cursor.execute("Select adsoyad From fiinfo")
            new_data = [a[0] for a in cursor.fetchall()]
            app.valuesfi = new_data

            self.ids.fullname_input_ekle.text = ""
            self.ids.fiweight_input_ekle.text = ""

            app.warn = "FI/Co-Pilot has been added to database successfully"
            show_popup()

            app.root.current = "anaekran"

    def tofiayarlar(self):
        app.root.current = "fiayarlar"

class FiUpdate(Screen):
    spinnerupdatefi = ObjectProperty()
    def filltextinputsfiupdate(self):
        adsoyad = self.ids.spinnerupdatefi.text
        if adsoyad == "Choose":
            self.ids.fullname_input_update.text = ""
            self.ids.weight_input_update.text = ""
        else:
            con = sqlite3.connect("database.db")
            cursor = con.cursor()
            cursor.execute("Select * From fiinfo where adsoyad = ?", (adsoyad,))
            fibilgiler = cursor.fetchall()
            fullname = fibilgiler[0][0]
            fiweight = fibilgiler[0][1]

            self.ids.fullname_input_update.text = str(fullname)
            self.ids.weight_input_update.text = str(fiweight)

    def updatetodbfi(self):
        adsoyad2 = self.ids.spinnerupdatefi.text
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute(
            "UPDATE fiinfo SET adsoyad = ?, fiweight = ? where adsoyad = ?",
            (self.ids.fullname_input_update.text, self.ids.weight_input_update.text, adsoyad2))
        con.commit()
        con.close()

        self.ids.fullname_input_update.text = ""
        self.ids.weight_input_update.text = ""


        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("Select adsoyad From fiinfo")
        new_data = [r[0] for r in cursor.fetchall()]
        app.valuesfi = new_data
        self.ids.spinnerupdatefi.text = "Choose"

        app.warn = "Update successful"
        show_popup()

        app.root.current = "anaekran"
    def tofiayarlar(self):
        app.root.current = "fiayarlar"

class FiSil(Screen):
    spinnerdeletefi = ObjectProperty()
    def filltextinputsfi(self):
        fidelete = self.ids.spinnerdeletefi.text
        if fidelete == "Choose":
            self.ids.deletefi_label.text = ""
            self.ids.delete_fi_label.text = ""
        else:
            self.ids.deletefi_label.text = "Delete   "
            self.ids.delete_fi_label.text = str(fidelete) + "  ?"

    def deletefromdbfi(self):
        fidelete2 = self.ids.spinnerdeletefi.text
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("Delete from fiinfo where adsoyad = ? ", (fidelete2,))
        con.commit()
        con.close()

        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("Select adsoyad From fiinfo")
        new_data = [r[0] for r in cursor.fetchall()]
        app.valuesfi = new_data

        self.ids.spinnerdeletefi.text = "Choose"

        app.warn = "FI/Co-Pilot deleted"
        show_popup()

        app.root.current = "anaekran"

    def tofiayarlar(self):
        self.ids.spinnerdeletefi.text = "Choose"
        app.root.current = "fiayarlar"


class WindowManager(ScreenManager):
    pass

class P(FloatLayout):
    pass

class MyApp(App):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute(
        "Create Table If not Exists ucaklar (registration TEXT, bem REAL, planearm REAL, sparm REAL, fiarm REAL, rs1arm REAL, rs2arm REAL, b1arm REAL, b2arm REAL, fuelarm REAL)")
    cursor.execute("Create Table If not Exists fiinfo (adsoyad TEXT, fiweight REAL)")
    con.commit()
    con.close()

    values = ListProperty()
    valuesfi = ListProperty()
    warn = "ASD"

    def build(self):
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("Select registration From ucaklar")
        ucaklist = [r[0] for r in cursor.fetchall()]
        self.values = ucaklist

        cursor.execute("Select adsoyad From fiinfo")
        filist = [r[0] for r in cursor.fetchall()]
        self.valuesfi = filist

        self.root = WindowManager()

def show_popup():
    show = P()
    popupWindow = Popup(title="Popup", content=show, size_hint=(None, None), size=(300, 150))
    popupWindow.open()

if __name__ == "__main__" :
    app = MyApp()
    app.run()




























