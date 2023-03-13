import numpy as np
import pickle

path1 = 'Heart_Disease/models/scaler.pkl'
path2 = 'Heart_Disease/models/model.pkl'
sc = pickle.load(open(path1, 'rb'))
model = pickle.load(open(path2, 'rb'))

def predict_disease(age,sex_,cp_,trestbps,chol,fbs_,restecg_,thalach,exang_,oldpeak,slope_,ca_,thal_):
    data = get_finaldata(age,sex_,cp_,trestbps,chol,fbs_,restecg_,thalach,exang_,oldpeak,slope_,ca_,thal_)
    prediction = model.predict(np.array([data]))
    if prediction[0] == 1:
        return "The person is suffering with Heart Disease."
    else:
        return "The person is not suffering with Heart Disease."


def get_finaldata(age,sex_,cp_,trestbps,chol,fbs_,restecg_,thalach,exang_,oldpeak,slope_,ca_,thal_):
    values = get_values(sex_,cp_,fbs_,restecg_,exang_,slope_,ca_,thal_)
    sex=values[0]
    cp=values[1]
    fbs=values[2]
    restecg=values[3]
    exang=values[4]
    slope=values[5]
    ca=values[6]
    thal=values[7]
    
    scaled_list = sc.transform([[age,trestbps,chol,thalach,oldpeak]])[0]
    gender_list = get_gender(sex)
    cp_list = get_cp(cp)
    fps_list=get_fps(fbs)
    restecg_list=get_restecg(restecg)
    exang_list = get_exang(exang)
    slope_list = get_slope(slope)
    ca_list = get_ca(ca)
    thal_list= get_thal(thal)

    final = list()
    final.extend(scaled_list)
    final.extend(gender_list)
    final.extend(cp_list)
    final.extend(fps_list)
    final.extend(restecg_list)
    final.extend(exang_list)
    final.extend(slope_list)
    final.extend(ca_list)
    final.extend(thal_list)
    return final


def get_gender(sex):
    glist=[0,0]
    if sex == 0:
        glist[0] = 1
    else:
        glist[1] = 1
    return list(glist)

def get_cp(cp):
    cplist = [0,0,0,0]
    if cp == 1:
        cplist[0]=1
    elif cp == 2:
        cplist[1]=1
    elif cp == 3:
        cplist[2]=1
    else:
        cplist[3]=1
    return list(cplist)

def get_fps(fbs):
    flist=[0,0]
    if fbs == 0:
        flist[0]=1
    else:
        flist[1]=1
    return list(flist)

def get_restecg(restecg):
    rlist=[0,0,0]
    if restecg == 0:
        rlist[0] = 1
    elif restecg == 1:
        rlist[1] = 1
    else:
        rlist[2] = 1
    return list(rlist)

def get_exang(exang):
    elist = [0,0]
    if exang == 0:
        elist[0] = 1
    else:
        elist[1] = 1
    return list(elist)

def get_slope(slope):
    slist = [0,0,0]
    if slope == 1:
        slist[0] = 1
    elif slope == 2:
        slist[1] = 1
    else:
        slist[2] = 1
    return list(slist)

def get_ca(ca):
    clist = [0,0,0,0]
    if ca == 0:
        clist[0] = 1
    elif ca == 1:
        clist[1] = 1
    elif ca == 2:
        clist[2] = 1
    else :
        clist[3] = 1
    return list(clist)

def get_thal(thal):
    tlist = [0,0,0]
    if thal == 3:
        tlist[0] = 1
    elif thal == 6:
        tlist[1] = 1
    else:
        tlist[2] = 1
    return list(tlist)

def get_values(sex_,cp_,fbs_,restecg_,exang_,slope_,ca_,thal_):
    if sex_ == 'Male':
        sex = 1
    else:
        sex = 0

    if cp_ == 'Typical angina':
        cp = 1
    elif cp_ == 'Atypical angina':
        cp = 2
    elif cp_ == 'Non-anginal pain':
        cp = 3
    else:
        cp = 4
        
    if fbs_ == 'No':
        fbs = 0
    else :
        fbs = 1

    if restecg_ == 'Normal':
        restecg = 0
    elif restecg_ ==  'ST-T wave abnormality':
        restecg = 1
    else:
        restecg = 2

    if exang_ == 'No':
        exang = 0
    else :
        exang = 1

    if slope_ == 'Upsloping':
        slope = 1
    elif slope_ == 'Flat':
        slope = 2
    else:
        slope = 3

    if ca_ == '0':
        ca = 0
    elif ca_ == '1':
        ca = 1
    elif ca_ == '2':
        ca = 2
    else:
        ca = 3

    if thal_ == 'Normal':
        thal = 3
    elif thal_ ==  'Fixed':
        thal = 6
    else:
        thal = 7

    return [sex,cp,fbs,restecg,exang,slope,ca,thal]


