def finalList(mainrank,perc,category,state,gender,pwd,limit,advrank):
    import pandas as pd
    from pathlib import Path
    from .rvp import pvr;

    base_path = Path(__file__).parent

    file_path = (base_path / "..//app//cleaned.csv").resolve()
   
    df = pd.read_csv(file_path)

    # The algorithm showed some anomaly when %tile was 100.
    # Hence the following condition.
    p_adv=pd.DataFrame()
    p_mains=pd.DataFrame()
    if( mainrank == '-1'):
        rank = float(pvr(perc,pwd,category))
    else:
        rank = mainrank     
    
    if(pwd == 'YES'):
        if(gender == 'M'):
            catg = category+'-PwD'
            if(rank > 0):
                p_mains = df[(df['Closing Rank']>=rank)&((df['Category']==catg)|(df['Category']=='OPEN-PwD'))&(df['Gender']=='Gender-Neutral')&(df['IIT']==0)]
            if(advrank > 0):
                p_adv = df[(df['Closing Rank']>=advrank)&((df['Category']==catg)|(df['Category']=='OPEN-PwD'))&(df['Gender']=='Gender-Neutral')&(df['IIT']==1)]
        else:
            catg = category+'-PwD'
            if(rank > 0):
                p_mains = df[(df['Closing Rank']>=rank)&((df['Category']==catg)|(df['Category']=='OPEN-PwD'))&(df['IIT']==0)]
            if(advrank > 0):
                p_adv = df[(df['Closing Rank']>=advrank)&((df['Category']==catg)|(df['Category']=='OPEN-PwD'))&(df['IIT']==1)]
    else:
        if(gender == 'M'):
            if(rank > 0):
                p_mains = df[(df['Closing Rank']>=rank)&((df['Category']==category)|(df['Category']=='OPEN'))&(df['Gender']=='Gender-Neutral')&(df['IIT']==0)]
            if(advrank > 0):
                p_adv = df[(df['Closing Rank']>=advrank)&((df['Category']==category)|(df['Category']=='OPEN'))&(df['Gender']=='Gender-Neutral')&(df['IIT']==1)]
        else:
            if(rank > 0): 
                p_mains = df[(df['Closing Rank']>=rank)&((df['Category']==category)|(df['Category']=='OPEN'))&(df['IIT']==0)]
            if(advrank > 0):
                 p_adv = df[(df['Closing Rank']>=advrank)&((df['Category']==category)|(df['Category']=='OPEN'))&(df['IIT']==1)]
    
    if(not p_adv.empty and (not p_mains.empty)):
        p = pd.concat([p_adv,p_mains])
    elif(not p_mains.empty):
        p = p_mains
    else:
        p=p_adv
     
    
    v = []
    for i in p.index:
        if(p['State'][i] == state):
            if(p['Quota'][i] != 'HS'):
                v.append(i)
        elif((p['Quota'][i] != 'OS') and (p['Quota'][i] != 'AI')):
                v.append(i)

    q = p .drop(index = v)
    if(q.shape[0] > 0):
        q = q.sort_values(by = 'Closing Rank')
        q = q[0:limit]
        x = q.drop(['Unnamed: 0','index','Category','Opening Rank','IIT','Round'],axis=1).drop_duplicates()
        x.reset_index(inplace = True, drop = True)
        return x
    else:
        return pd.DataFrame()
