from cod_api import API, platforms
import asyncio
from flask import Flask,request
from flask_jsonpify import jsonify
import requests
import json
import urllib.parse

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def api():
    try:
        
            request_data = request.get_json()
            user = request_data['user']
            acc = request_data['acc']
            game = request_data['game']
            
            print(game)

            if game == 1:
                
                api = API()
                api.login('TOKEN')  
                
            
                if(acc == 1):  
                    res = api.Warzone.fullData(platforms.Battlenet, user) 
                elif(acc == 2):
                    res = api.Warzone.fullData(platforms.Activision, user) 
                elif(acc == 3):
                    res = api.Warzone.fullData(platforms.PSN, user) 
                elif(acc == 4):
                    res = api.Warzone.fullData(platforms.XBOX, user)
                else:
                    res = api.Warzone.fullData(platforms.All, user)
                   
                if 'message' in res['data']:
                    if 'user not found' in res['data']['message']:
                        found = 1    
                else:
                    found = 0
                
                if found != 1 :
                    
                    url = "https://api.wzhub.gg/api/modes/"+ urllib.parse.quote(user, safe="") + "/battle/wz1?lang=pt"
                    response = requests.request("GET", url)
                    responsejson = json.loads(response.text)
                
                    
                    
                    wzkdRatio = responsejson['caldera']['kd']
                    wzwins = responsejson['caldera']['wins']
                    wzkills = responsejson['caldera']['kills']
                    wzdeaths = responsejson['caldera']['deaths']
                    
                    
                    rebirthkdRatio = responsejson['rebirth']['kd']
                    rebirthwins = responsejson['rebirth']['wins']
                    rebirthkills = responsejson['rebirth']['kills']
                    rebirthdeaths = responsejson['rebirth']['deaths']
                    
                    
                    
                    fortkeepkdRatio = responsejson['fortkeep']['kd']
                    fortkeepwins = responsejson['fortkeep']['wins']
                    
                    
                    fortkeepkills = responsejson['fortkeep']['kills']
                    fortkeepdeaths = responsejson['fortkeep']['deaths']
                    
               
    
                    plunderkdRatio = res['data']['lifetime']['mode']['br_dmz']['properties']['kdRatio']
                    plunderwins = res['data']['lifetime']['mode']['br_dmz']['properties']['wins']
                    plunderkills = res['data']['lifetime']['mode']['br_dmz']['properties']['kills']
                    plunderdeaths = res['data']['lifetime']['mode']['br_dmz']['properties']['deaths']
                    
            
                    # printing results to console
                    main ={}
                    Infos ={}
                    Infos['name'] = 'Batle Royale'
                    Infos['kdRatio'] = wzkdRatio
                    Infos['wins'] = wzwins
                    Infos['kills'] = wzkills
                    Infos['deaths'] = wzdeaths
                    main['wz'] = Infos
                    Infos ={}
                    Infos['name'] = 'Plunder'
                    Infos['kdRatio'] = plunderkdRatio
                    Infos['wins'] = plunderwins
                    Infos['kills'] = plunderkills
                    Infos['deaths'] = plunderdeaths
                    main['plunder'] = Infos
                    Infos ={}
                    Infos['name'] = 'Rebirth'
                    Infos['kdRatio'] = rebirthkdRatio
                    Infos['wins'] = rebirthwins
                    Infos['kills'] = rebirthkills
                    Infos['deaths'] = rebirthdeaths
                    main['rebirth'] = Infos
                    Infos ={}
                    Infos['name'] = 'Fortkeep'
                    Infos['kdRatio'] = fortkeepkdRatio
                    Infos['wins'] = fortkeepwins
                    Infos['kills'] = fortkeepkills
                    Infos['deaths'] = fortkeepdeaths
                    main['fortkeep'] = Infos
    
    
                    return jsonify(main)
                
                else:
                    main ={}
                    main['res'] = '0'
                    return jsonify(main)
                
            else:
                main ={}
                main['game'] = '0'
                return jsonify(main)
            
            
            
    except Exception as err:
       print(err)

@app.route("/match", methods=['GET', 'POST'])
def  matches():
    try:
        request_data = request.get_json()
        
        user = request_data['user']
        game = request_data['game']
        print(user)
        print(game)
        
        if game == 1:
            
            url = "https://api.wzhub.gg/api/matches/"+ urllib.parse.quote(user, safe="") + "/battle/wz1?lang=en"
            response = requests.request("GET", url)
            print(response.text)
            main = json.loads(response.text)
            
            return jsonify(main)
        else:
            main ={}
            main['game'] = '0'
            return jsonify(main)
    
        print(main)
    except Exception as err:
       print(err)

@app.route("/leader", methods=['GET', 'POST'])
def leaderboard():
    
    try:
        url = "https://app.wzstats.gg/leaderboard/teamKillRecords/?map=CALDERA&mode=STANDARD_BR&teamSize=4&playersCount=4"
        response = requests.request("GET", url)
        main = json.loads(response.text)
        print(main)
        return jsonify(main)
    
    except Exception as err:
       print(err)


    


if __name__ == '__main__':
      app.run(host='192.168.15.33', port=80)
