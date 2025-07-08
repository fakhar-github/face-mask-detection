import xmltodict
import os
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import matplotlib.patches as mpatches
from collections import Counter

def data_visualization(
        image_name: str, 
        data_dir: str, 
        ax: Axes
    ):
    with open(f'{data_dir}/annotations/' + image_name[:-4]+".xml") as fd:
        doc = xmltodict.parse(fd.read())
    image = plt.imread(os.path.join(f'{data_dir}/images/' + image_name))
    ax.axis("off")
    temp = doc["annotation"]["object"]
    if type(temp)==list:
        for i in range(len(temp)):
            ###with_mask
            if temp[i]["name"]=="with_mask":
                x,y,w,h=list(map(int,temp[i]["bndbox"].values()))
                mpatch=mpatches.Rectangle((x,y),w-x,h-y,linewidth=1, edgecolor='g',facecolor="none",lw=2,)
                ax.add_patch(mpatch)
                rx, ry = mpatch.get_xy()
            ###without_mask
            if temp[i]["name"]=="without_mask":
                x,y,w,h=list(map(int,temp[i]["bndbox"].values()))     
                mpatch=mpatches.Rectangle((x,y),w-x,h-y,linewidth=1, edgecolor='r',facecolor="none",lw=2,)
                ax.add_patch(mpatch)
                rx, ry = mpatch.get_xy()
            ###mask_weared_incorrect
            if temp[i]["name"]=="mask_weared_incorrect":
                x,y,w,h=list(map(int,temp[i]["bndbox"].values()))
                mpatch=mpatches.Rectangle((x,y),w-x,h-y,linewidth=1, edgecolor='y',facecolor="none",lw=2,)
                ax.add_patch(mpatch)
                rx, ry = mpatch.get_xy()
    else:
        x,y,w,h=list(map(int,temp["bndbox"].values()))
        edgecolor={"with_mask":"g","without_mask":"r","mask_weared_incorrect":"y"}
        mpatch=mpatches.Rectangle((x,y),w-x,h-y,linewidth=1, edgecolor=edgecolor[temp["name"]],facecolor="none",)
    ax.imshow(image)
    ax.add_patch(mpatch)

def data_analysis(
        data_dir: str
    ):
    image_names = os.listdir(f'{data_dir}/images')
    data = []
    for image_name in image_names[:]:
        with open(f'{data_dir}/annotations/' + image_name[:-4]+".xml") as fd:
            doc=xmltodict.parse(fd.read())
        temp=doc["annotation"]["object"]
        if type(temp)==list:
            for i in range(len(temp)):
                data.append(temp[i]["name"])
        else:
            data.append(temp["name"])
        
    data = Counter(data)
    for key, value in data.items():
        print(f'{key}:', value)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize =(14,6))
    colors = { 'with_mask': 'g',
                'mask_weared_incorrect': 'y',
                'without_mask': 'r'
            }
    ax1.pie(
        list(data.values()), 
        wedgeprops = dict(width=0.3, edgecolor='w') ,
        labels = list(data.keys()), 
        radius=1, 
        startangle = 120, 
        autopct='%1.2f%%',
        colors = [colors[key] for key in data.keys()]
    )

    ax2.bar(
        list(data.keys()),
        list(data.values()),
        width = 0.4
    )

    plt.show()


def datapreprocessing(
        data_dir: str = None,
        visualize_data: bool = True,
        analyze_data: bool = True
    ):
    if data_dir is None:
        raise ValueError('Data directory should not be none')
    
    xml_names = os.listdir(f'{data_dir}/annotations') 
    image_names = os.listdir(f'{data_dir}/images')

    if analyze_data:
        data_analysis(data_dir = data_dir)

    if visualize_data:
        fig,ax=plt.subplots(2, 2)
        fig.set_size_inches(10,10)
        data_visualization(image_name=image_names[0], data_dir=data_dir, ax=ax[0,0])
        data_visualization(image_name=image_names[10], data_dir=data_dir, ax=ax[0,1])
        data_visualization(image_name=image_names[20], data_dir=data_dir, ax=ax[1,0])
        data_visualization(image_name=image_names[5], data_dir=data_dir, ax=ax[1,1])
    
    return image_names, xml_names

