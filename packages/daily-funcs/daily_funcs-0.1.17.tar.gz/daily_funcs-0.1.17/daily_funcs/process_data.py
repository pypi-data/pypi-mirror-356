import json
import pandas as pd
from tqdm import tqdm
import math
import datetime
def read_data(file_path,input_type=None,return_type='json'):
    if input_type is None:
        input_type = file_path.split('.')[-1]
    if input_type == 'jsonl':
        with open(file_path,'r') as fp:
            data = []
            for line in fp.readlines():
                item = json.loads(line)
                data.append(item)
    elif input_type == 'json':
        with open(file_path,'r') as fp:
            data = json.load(fp)
    elif input_type == 'csv':
        df = pd.read_csv(file_path)
        # 转换为JSON格式
        # 使用`to_json()`方法，指定`orient`参数以控制JSON格式
        data = df.to_json(orient='records', lines=True)
        data = [json.loads(line) for line in data.splitlines()]
    elif input_type == 'parquet':
        data = pd.read_parquet(file_path)
    elif input_type == 'pickle':
        data = pd.read_pickle(file_path)
    elif input_type == 'feather':
        data = pd.read_feather(file_path)
    elif input_type == 'hdf5':
        data = pd.read_hdf(file_path)
    elif input_type == 'xlsx':
        df = pd.read_excel(file_path)
        data = json.loads(df.to_json(orient='records', force_ascii=False))
    else:
        raise ValueError(f"Unsupported input type: {input_type}")
    if return_type == 'csv':
        return data.to_csv(index=False)
    return data

def save_data(data,file_path,output_type=None):
    if output_type is None:
        output_type = file_path.split('.')[-1]
    if output_type == 'jsonl':
        with open(file_path,'w') as fp:
            for item in data:
                fp.write(json.dumps(item,ensure_ascii=False) + '\n')
    elif output_type == 'json':
        with open(file_path,'w') as fp:
            json.dump(data,fp,ensure_ascii=False,indent=2)
    elif output_type == 'csv':
        data.to_csv(file_path,index=False)
    else:
        raise ValueError(f"Unsupported output type: {output_type}")


def read_data_odps(path,selected_cols='',batch_size=2048):
    import common_io
    reader = common_io.table.TableReader(path,
                                        slice_id=0,
                                        slice_count=1,
                                        num_threads=12,
                                        selected_cols=selected_cols,
                                        capacity=2048)
    total_records_num = reader.get_row_count()
    print("total_records_num:", total_records_num)
    data = []
    batch_num = math.ceil(total_records_num / batch_size)
    values = []
    if selected_cols != '':
        selected_cols_list = selected_cols.split(',')
        for i in tqdm(range(0, batch_num)):
            records = reader.read(batch_size, allow_smaller_final_batch=True)
            for item in records:
                new_item = {}
                for j in range(len(selected_cols_list)):
                    new_item[selected_cols_list[j]] = item[j]
                data.append(new_item)
    else:
        for i in tqdm(range(0, batch_num)):
            records = reader.read(batch_size, allow_smaller_final_batch=True)
            for item in records:
                data.append(item)
    return data



def upload2odps(data, outputs, slice_id=0, batch_size=2048):
    import common_io
    with common_io.table.TableWriter(outputs, slice_id=slice_id) as table_writer:
        values = []
        count_unicode_decode_error = 0
        total_records_num = len(data)
        batch_num = math.ceil(total_records_num / batch_size)
        for i in range(0, batch_num):
            records = data[i * batch_size:(i+1)* batch_size]
            # 定义其字段
            keys = records[0].keys()
            for item in records:
                values.append(list(item.values()))
            if i == 0:
                print(values[:1])

            if (i+1)%10==0 and (i+1)%50!=0:
                print(f"[{datetime.datetime.now()}] {i + 1}/{batch_num} batches processed. current row num is {len(values)}")

            if (i + 1) % 50 == 0:
                print (values[:1])
                print(f"[{datetime.datetime.now()}] {i + 1}/{batch_num} batches write to table.")
                table_writer.write(values, col_indices=tuple(range(0,len(keys))))
                values = []
                
        if (len(values)>0):
            table_writer.write(values, col_indices=tuple(range(0,len(keys))))
            print(f"[{datetime.datetime.now()}] {i + 1}/{batch_num} batches write to table sucess.")
