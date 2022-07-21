
from random import randint
import dtlpy as dl

if __name__ == '__main__':
    dataset = dl.datasets.get(dataset_id='Dataset_ID')
    count = 0
    customers = ['dataloop', 'customer2', 'customer3', 'customer4']
    regions = ['Asia', 'Africa', 'Western Europe', 'Middle East']
    geoNames = ['Israel', 'Japan', 'India', 'France']
    files = [11998, 11999, 12000, 12001]
    devises = ['macOS', 'Android', 'Windows', 'Linux']
    models = ['yolo', 'R-CNN', 'MaskRNN', 'Tensorflow']

    for page in dataset.items.list():
        for item in page:
            if count >= 4:
                count = 0
            item.metadata['user'] = dict()
            item.metadata['user']['customer_name'] = customers[count]
            item.metadata['user']['region'] = regions[count]
            item.metadata['user']['geoName'] = geoNames[count]
            item.metadata['user']['file_number'] = files[count]
            item.metadata['user']['deviceDetails'] = dict()
            item.metadata['user']['deviceDetails']['deviceOsType'] = devises[count]
            item.metadata['user']['model'] = dict()
            item.metadata['user']['model']['name'] = models[count]
            item.metadata['user']['HaveLabResults'] = True if count <= 2 else False
            item.metadata['user']['Type'] = randint(1, 10)
            item.update()
            count += 1
