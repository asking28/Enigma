import numpy as np
import pandas as pd
from pandas import read_csv
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
user_data=read_csv('user_data.csv')
print(user_data.shape)
print(user_data.head(10))
problem_data=read_csv('problem_data.csv')
print(problem_data.shape)
print(problem_data.head(10))
train_submissions=read_csv('train_submissions.csv')
print(train_submissions.head(2))
print(train_submissions.shape)
test_submissions=read_csv('test_submissions.csv')
test_merge=test_submissions.merge(user_data,how='left',on='user_id')
test_merging=test_merge.merge(problem_data,how='left',on='problem_id')
user_merge=train_submissions.merge(user_data,how='left',on='user_id')
#print(user_merge.shape)
#print(user_merge.head(3))
problem_user_merge=user_merge.merge(problem_data,how='left',on='problem_id')
#print(problem_user_merge.shape)
print(problem_user_merge.head(5))
problem_user_merge=problem_user_merge.drop(['country'],axis=1)
#print(problem_user_merge.head(1))

#problem_user_merge['country']=problem_user_merge['country'].fillna(problem_user_merge['country'].mode(),inplace=True)
le=LabelEncoder()
problem_user_merge['rank']=le.fit_transform(problem_user_merge['rank'])
problem_user_merge=pd.DataFrame(problem_user_merge)
test_merging['rank']=le.fit_transform(test_merging['rank'])
test_merging=pd.DataFrame(test_merging)
#print(problem_user_merge.head(10))
problem_user_merge['points']=problem_user_merge['points'].fillna(problem_user_merge['points'].mean())
test_merging['points']=test_merging['points'].fillna(test_merging['points'].mean())
#problem_user_merge['level_type']=problem_user_merge['level_type'].fillna(problem_user_merge['level_type'].dropna().mode(),inplace=True)
#print(problem_user_merge.head(10))
problem_user_merge=problem_user_merge.dropna(subset=['level_type'])
problem_user_merge['level_type']=le.fit_transform(problem_user_merge['level_type'])
problem_user_merge=pd.DataFrame(problem_user_merge)
#print(problem_user_merge.head(5))
#problem_user_merge=problem_user_merge.drop(['level_type'],axis=1)
problem_user_merge['level_type']=problem_user_merge['level_type'].replace(np.NaN,'A')
#test_merging=test_merging.drop(['level_type'],axis=1)
test_merging=test_merging.drop(['tags'],axis=1)
test_merging['level_type']=test_merging['level_type'].replace(np.NaN,'A')
test_merging['level_type']=le.fit_transform(test_merging['level_type'])
print(problem_user_merge.head(2))
feature_columns_to_use=['submission_count','problem_solved','contribution','follower_count','last_online_time_seconds','max_rating','rating','rank','registration_time_seconds','points','level_type']
train_X=problem_user_merge[feature_columns_to_use]
train_Y=problem_user_merge['attempts_range']
test_X=test_merging[feature_columns_to_use]
print(train_X.head(2))
print(test_X.shape)
gbm=xgb.XGBClassifier(max_depth=12,n_estimators=1000,learning_rate=0.25).fit(train_X,train_Y)
print(pd.DataFrame(test_X).head(3))
predictions=gbm.predict(test_X)
predictions=[round(value) for value in predictions]
submission1=pd.DataFrame({'ID':test_submissions['ID'],'attempts_range':predictions})
submission1.to_csv("submission2.csv",index=False)
