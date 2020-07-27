import numpy as np
import cv2
import seaborn as sns
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
from math import sqrt
from datetime import datetime
import matplotlib.dates as mdates
from scipy import stats

def canny_edge(in_filename):
    img = cv2.imread(in_filename,0)

    gray_filtered = cv2.bilateralFilter(img, 10, 50, 50)

    # Using the Canny filter to get contours
    edges = cv2.Canny(gray_filtered, 20, 30)
    # Using the Canny filter with different parameters
    edges_high_thresh = cv2.Canny(gray_filtered, 60, 120)
    # Stacking the images to print them together
    # For comparison
    images = np.hstack((img, edges, edges_high_thresh))
    # Output the resulting

    cv2.imwrite('images/canny_img/canny_'+ \
                 os.path.splitext(os.path.basename(in_filename))[0] + \
                 '.png',images)
    return edges_high_thresh

def contours_metadata(contours):
    ##將contours的metadata存入contours_data
    contours_data={}
    cnts_perimeter=[]
    cnts_area=[]
    cnts_index=[]

    ## 計算資料分布改框的條件，因為小於200的資料太多，故刪除
    for c in contours:
        if cv2.contourArea(c)>200.0 and \
           cv2.arcLength(c,False)<600 :
            cnts_index.append(c)
            cnts_perimeter.append(cv2.arcLength(c,False))
            cnts_area.append(cv2.contourArea(c))
    contours_data['index']=cnts_index
    contours_data['perimeter']=cnts_perimeter
    contours_data['area']=cnts_area
    # show_statistic(contours_data['area'],25.0)

    # plt.hist(contours_data['area'], color = 'blue', edgecolor = 'black'
    #          ,bins = int((max(contours_data['area'])-min(contours_data['area']))/25.0))
    contours_data['area_avg']=np.average(contours_data['area'])
    contours_data['area_variance']=np.var(contours_data['area'])
    contours_data['area_std']=np.std(contours_data['area'])
    bp_dict=plt.boxplot(contours_data['area'])

    contours_data['area_Q1']=[item.get_ydata()[1] for item in bp_dict['boxes']][0]
    contours_data['area_Q3']=[item.get_ydata()[3] for item in bp_dict['boxes']][0]
    contours_data['area_median']=[item.get_ydata()[1] for item in bp_dict['medians']][0]
    contours_data['area_min']=[item.get_ydata()[1] for item in bp_dict['whiskers']][0]
    contours_data['area_max']=[item.get_ydata()[1] for item in bp_dict['whiskers']][1]

    plt.clf()
    plt.close()
    # print("25%: ",contours_data['area_Q1'])
    # print("75%: ",contours_data['area_Q3'])
    # print("median: ",contours_data['area_median'])
    # print("min",contours_data['area_min'])
    # print("max",contours_data['area_max'])

    return contours_data


def BananaContours():
    directory="images/edged_img/"
    datetime_objects=[]
    files=[]
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            datetime_objects.append(datetime.strptime(filename,"image_%d-%m-%Y_%I-%M-%S_%p.png"))
            # print("--",os.path.join(directory,filename))

    datetime_objects=sorted(datetime_objects)
    for d in datetime_objects:
        filename=d.strftime("image_%d-%m-%Y_%I-%M-%S_%p.png")
        files.append(os.path.join(directory,filename))
    banana_volume_list=[]
    for f in files:
        # edges = canny_edge(f)
        #ret,thresh = cv2.threshold(edges,127,255,0)
        img = cv2.imread(f,0)
        #ret,thresh = cv2.threshold(img,127,255,0)
        blurred = cv2.GaussianBlur(img, (5, 5), 0)
        value, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)

        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        metadata = contours_metadata(contours)
        median =metadata['area_median']
        maximum =metadata['area_max']
        area_avg = metadata['area_avg']
        area_std = metadata['area_std']
        q1=metadata['area_Q1']
        cnt_with_area =[]
        total_area = 0.0
        # /** 針對average、standard deviation去篩選contours */
        # for c in contours:
            # if cv2.contourArea(c)>(q1)and \
            # cv2.contourArea(c)<(area_avg+0.25*area_std)and\
            #     cv2.arcLength(c,False)<600:
            # cnt_with_area.append(c)
            # total_area += cv2.contourArea(c)

        c = max(contours, key = cv2.contourArea)
        cnt_with_area.append(c)
        total_area += cv2.contourArea(c)
        print(len(cnt_with_area))
        # print(len(cnt_with_area))

        # /** 使用Q1、medina、Q3來篩選contours
        # for c in contours:
        #     if cv2.contourArea(c)> median and \
        #         cv2.contourArea(c)< maximum :
        #         cnt_with_area.append(c)
        #         total_area += cv2.contourArea(c)

        read_filename = directory+ \
                        os.path.splitext(os.path.basename(f))[0] +\
                    '.png'
        out_filename = 'images/result_pics/res_' + os.path.splitext(os.path.basename(f))[0] + '.png'
        result = cv2.drawContours(cv2.imread(read_filename), cnt_with_area, -1, (0,0,255), 2)
        cv2.imwrite(out_filename, result)

        ## 畫圖
        # if len(cnt_with_area)!=0.0:
        avg_area=total_area / len(cnt_with_area)
        banana_volume=sqrt(avg_area)**3
        banana_volume_list.append(banana_volume)

    x = list(range(1, len(banana_volume_list)+1))

    x = [ i.toordinal() for i in datetime_objects ]
    y_dots = banana_volume_list
    print(y_dots)
    def myfunc(x):
        return slope * x + intercept

    slope, intercept, r, p, std_err = stats.linregress(x, y_dots)
    y_regression = list(map(myfunc, x))

    ax = plt.gca()
    formatter = mdates.DateFormatter("%b")
    ax.xaxis.set_major_formatter(formatter)

    locator = mdates.MonthLocator()
    ax.xaxis.set_major_locator(locator)

    formatter = mdates.DateFormatter("%d")
    ax.xaxis.set_minor_formatter(formatter)

    locator = mdates.DayLocator()
    ax.xaxis.set_minor_locator(locator)

    ax.set_xlim([datetime(2020, 6, 10), datetime(2020, 7, 13)])

    ax.scatter(x, y_dots)
    ax.plot(x, y_regression)
    plt.savefig("scatter.png")

    # plt.show()
