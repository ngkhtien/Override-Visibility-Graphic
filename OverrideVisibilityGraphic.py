"""Change template to nomination template then return back to previous template. Nomination template will override Visibility/Graphic that not controlled by previous template"""
__author__='NguyenKhanhTien - khtien0107@gmail.com'
from Autodesk.Revit.DB import ViewSheet, Transaction, View, TransactionGroup
from pyrevit import revit, DB
from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document

viewsheet = forms.select_sheets(button_name='Select Sheet Set')

selected_viewtemplates = forms.select_viewtemplates(doc=revit.doc)
temp=selected_viewtemplates[0].Id
save_tem = []
views = []
count=0
print("View from sheets:")
for sheet in viewsheet:
    print (sheet.Title)

print("------------------------------------------------------------------------------")
print("Changing view template to: " + str(selected_viewtemplates[0].Name))

tg = TransactionGroup(doc, "Update Template")
tg.Start()

t=Transaction(doc,"Change Template")
t.Start()
for vs in viewsheet:
    for eid in vs.GetAllPlacedViews():
        ev=doc.GetElement(eid)
        if str(ev.ViewType) != "Legend" and str(ev.ViewType) != "DraftingView":
            tam=ev.ViewTemplateId
            if str(tam) != ("-1"):
                ev.ViewTemplateId = temp
                views.append(ev)
                save_tem.append(tam)
                count+=1
            else:
                ev.ViewTemplateId = temp
t.Commit()
print("------------------------------------------------------------------------------")
print("Backing to previous view template")
print("------------------------------------------------------------------------------")
t=Transaction(doc,"Return Template")
t.Start()
x=0
for i in views:
    i.ViewTemplateId = save_tem[x]
    x+=1
t.Commit()

tg.Assimilate()
print ("COMPLETED!!!")