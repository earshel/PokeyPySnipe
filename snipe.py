#!/usr/bin/python
import argparse
import logging
import time
import sys
import json
import configparser
from POGOProtos.Enums import PokemonMove_pb2
from custom_exceptions import GeneralPogoException

from api import PokeAuthSession
from location import Location

from pokedex import pokedex
from inventory import items
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for
from flask import jsonify
import thread
import subprocess
import os
import sys


app = Flask(__name__)

@app.route('/_snipe_')
def remote_Snipe():
    global ignoreCP
    
    snipecoords = request.args.get('snipecoords', 0)
    pokemonName = request.args.get('pokemonName', 0)
    igCP = request.args.get('ignoreCP',0)
    
    if str(igCP) == str('ignoreCP'):
        
        ignoreCP  = True
    else:
        
        ignoreCP = False
        

    
    doSnipe(session,config,snipecoords,pokemonName)
   
    
    
    return render_template('result.html')


@app.route('/release')
def release():
    inventory = session.getInventory()
    
    #id: 2436312686824190668
    #pokemon_id: EEVEE
    #cp: 46
    #stamina: 19
    #stamina_max: 19
    #move_1: TACKLE_FAST
    #move_2: DIG
    #height_m: 0.297532558441
    #weight_kg: 8.24643802643
    #individual_attack: 15
    #individual_defense: 12
    #individual_stamina: 9
    #cp_multiplier: 0.166397869587
    #pokeball: ITEM_POKE_BALL
    #captured_cell_id: 6108423709528162304
    #creation_time_ms: 1469364470778
    pokeID = request.args.get('pokeID', 0)
    action = request.args.get('action',0)
    
    
    
    for z in pokeID.split(","):
        
    
        for poke in range(0,len(inventory.party)-1):
            curPoke = inventory.party[poke]
            #logging.critical(str(curPoke.id) + "," + str(z))
            
            if str(curPoke.id) == str(z):
                
                
                
                if action.find("Release") > -1:
                    logging.critical("Found pokemon. Transfer in progress...")
                    logging.critical(session.releasePokemon(inventory.party[poke]))
                elif action.find("Evolve") > -1:
                    logging.critical("Found pokemon. Evolve in progress...")
                    logging.critical(session.evolvePokemon(inventory.party[poke]))
                    
                time.sleep(1)
    return render_template('inventoryTimeout.html')
    

@app.route('/inventory')
def inventory():
    inventory = session.getInventory()
    pokes = []
    #id: 2436312686824190668
    #pokemon_id: EEVEE
    #cp: 46
    #stamina: 19
    #stamina_max: 19
    #move_1: TACKLE_FAST
    #move_2: DIG
    #height_m: 0.297532558441
    #weight_kg: 8.24643802643
    #individual_attack: 15
    #individual_defense: 12
    #individual_stamina: 9
    #cp_multiplier: 0.166397869587
    #pokeball: ITEM_POKE_BALL
    #captured_cell_id: 6108423709528162304
    #creation_time_ms: 1469364470778
    
    
    for poke in range(0,len(inventory.party)-1):
        
    
        family = {'1': {1,2,3},'4': {4,5,6},'7': {7,8,9}, '10': {10,11,12}, '13': {13,14,15}, '16': {16,17,18}, '19': {19,20}, '21': {21,22}, '23': {23,24},'25': {25,26}, '27': {27,28}, '29': {29,30,31}, '32': {32,33,34}, '35': {35,36}, '37': {37,38}, '39': {39,40}, '41': {41,42}, '43': {43,44,45}, '46': {46,47}, '48': {48,49}, '50': {50,51}, '52': {52,53},'54': {54,55}, '56': {56,57}, '58': {58,59}, '60': {60,61,62}, '63': {63,64,65}, '66': {66,67,68},'69': {69,70,71}, '72': {72,73}, '74': {74,75,76}, '77': {77,78}, '79': {79,80}, '81': {81,82,83}, '84': {84,85}, '86': {86,87}, '88': {88,89}, '90': {90,91}, '92': {92,93,94}, '95': {95}, '96': {96,97}, '98': {98,99}, '100': {100,101}, '102': {102,103}, '104': {104,105}, '106': {106}, '107': {107},'108': {108}, '109': {109,110}, '111': {111,112}, '113': {113}, '114': {114}, '115': {115}, '116': {116,117}, '118': {118,119}, '120': {120,121},'122': {122}, '123': {123}, '124': {124}, '125': {125}, '126': {126}, '127': {127}, '128': {128}, '129': {129,130}, '131': {131}, '132': {132}, '133': {133,134,135,136},'137': {137}, '138': {138,139}, '140': {140,141},'142': {142}, '143': {143}, '144': {144}, '145': {145}, '146':{146}, '147': {147,148,149}, '150': {150}, '151': {151}}
        reqCandy = {'1':25,'2':100,'3':0,'4':25,'5':100,'6':0,'7':25,'8':100,'9':0,'10':12,'11':50,'12':0,'13':12,'14':50,'15':0,'16':12,'17':50,'18':0,'19':25,'20':0,'21':50,'22':0,'23':50,'24':0,'25':50,'26':0,'27':50,'28':0,'29':25,'30':100,'31':0,'32':25,'33':100,'34':0,'35':50,'36':0,'37':50,'38':0,'39':50,'40':0,'41':50,'42':0,'43':25,'44':100,'45':0,'46':50,'47':0,'48':50,'49':0,'50':50,'51':0,'52':50,'53':0,'54':50,'55':0,'56':50,'57':0,'58':50,'59':0,'60':25,'61':100,'62':0,'63':25,'64':100,'65':0,'66':25,'67':100,'68':0,'69':25,'70':100,'71':0,'72':50,'73':0,'74':25,'75':100,'76':0,'77':50,'78':0,'79':50,'80':0,'81':50,'82':0,'83':0,'84':50,'85':0,'86':50,'87':0,'88':50,'89':0,'90':50,'91':0,'92':25,'93':100,'94':0,'95':0,'96':50,'97':0,'98':50,'99':0,'100':50,'101':0,'102':50,'103':0,'104':50,'105':0,'106':0,'107':0,'108':0,'109':50,'110':0,'111':50,'112':0,'113':0,'114':0,'115':0,'116':50,'117':0,'118':50,'119':0,'120':50,'121':0,'122':0,'123':0,'124':0,'125':0,'126':0,'127':0,'128':0,'129':400,'130':0,'131':0,'132':0,'133':25,'134':0,'135':0,'136':0,'137':0,'138':50,'139':0,'140':50,'141':0,'142':0,'143':0,'144':0,'145':0,'146':0,'147':25,'148':100,'149':0,'150':0,'151':0}
        
        curPoke = inventory.party[poke]   
        candies = 0
        if str(curPoke.pokemon_id) not in family:
            
            for z in family:
                
                if curPoke.pokemon_id in family[z]:
                    #logging.critical(str(pokedex[curPoke.pokemon_id]) + " is in family " +str(z))
                    #logging.critical(inventory.candies)
                    candies = inventory.candies[int(z)]
        else:
            #logging.critical(str(curPoke.pokemon_id) + " is a family!")
            candies = inventory.candies[curPoke.pokemon_id]
        
            
        pokez = {
        'id': str(curPoke.id),
        'pokemon_id': curPoke.pokemon_id,
        'pokemon_name': pokedex[curPoke.pokemon_id],
        'cp': curPoke.cp,
        'stamina': curPoke.stamina,
        'stamina_max': curPoke.stamina_max,
        'move_1': curPoke.move_1,
        'move_2': curPoke.move_2,
        'height_m': curPoke.height_m,
        'weight_kg': curPoke.weight_kg,
        'individual_attack': curPoke.individual_attack,
        'individual_defense': curPoke.individual_defense,
        'individual_stamina': curPoke.individual_stamina,
        'candies': candies,
        'reqCandies': reqCandy[str(curPoke.pokemon_id)]
        }
        pokes.append(pokez)
        
        
    
    
    
    json.dump(pokes, open('static/inventory.json', 'w'))
    
    return render_template('inventory.html')
    
@app.route('/')
def index():
    
    stats = session.getInventory().stats
    profileInfo = session.getProfile().player_data

        #level
        #experience: 2004695
        #prev_level_xp: 1650000
        #next_level_xp: 2500000
        #km_walked: 29.3902397156
        #pokemons_encountered: 4484
        #unique_pokedex_entries: 92
        #pokemons_captured: 4348
        #evolutions: 614
        #poke_stop_visits: 13337
        #pokeballs_thrown: 4819
        #eggs_hatched: 7
    
    
    if profileInfo.team:
        
        team = profileInfo.team
    else:
        team = 'noteam'
               
    statz = {
    'level': str(stats.level),
    'experience': str(stats.experience),
    'next_level_xp': str(stats.next_level_xp),
    'km_walked': str(stats.km_walked),
    'pokemons_encountered': str(stats.pokemons_encountered),
    'pokemons_captured': str(stats.pokemons_captured),
    'username': str(profileInfo.username),
    'max_pokemon_storage': str(profileInfo.max_pokemon_storage),
    'max_item_storage': str(profileInfo.max_item_storage),
    'team': team
    
    
    
                }
        
        
        
    
    
    
    json.dump(statz, open('static/stats.json', 'w'))
    

    return render_template('dashboard.html')
    

@app.route('/snipe')
def snipez():
    
    
    return render_template('snipe.html')
    


@app.errorhandler(500)
def page_not_found(e):
    return render_template('result.html'), 404

    
def setupLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('Line %(lineno)d,%(filename)s - %(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)



# Get profile
def getProfile(session):
        logging.info("Printing Profile:")
        profile = session.getProfile()
        logging.info(profile)


# Grab the nearest pokemon details
def findBestPokemon(session,config,firstTry,pokemonName):
    # Get Map details and print pokemon
    logging.info("Finding Nearby Pokemon:")
    logging.info("Due to recent request throttling, we have to wait 10 sec here to be sure that we get a populated getMapObjects.")
    time.sleep(10)
    cells = session.getMapObjects()
    closest = float("Inf")
    best = -1
    pokemonBest = None
   
    latitude, longitude, _ = session.getCoordinates()
    logging.info("Current pos: %f, %f" % (latitude, longitude))
    for cell in cells.map_cells:
        # Heap in pokemon protos where we have long + lat
        pokemons = [p for p in cell.wild_pokemons] + [p for p in cell.catchable_pokemons]
        for pokemon in pokemons:
            # Normalize the ID from different protos
            pokemonId = getattr(pokemon, "pokemon_id", None)
            if not pokemonId:
                pokemonId = pokemon.pokemon_data.pokemon_id
            if pokedex[pokemonId].upper() == pokemonName.upper():
                pokemonBest = pokemon
                logging.info("Hey, we found the Pokemon you looks for!")
                break
            # Find distance to pokemon
            dist = Location.getDistance(
                latitude,
                longitude,
                pokemon.latitude,
                pokemon.longitude
            )

            # Log the pokemon found
            logging.info("Found a %s, %f meters away \n" % (
                pokedex[pokemonId],
                dist
            ))

            rarity = pokedex.getRarityById(pokemonId)
            # Greedy for rarest
            if rarity > best:
                pokemonBest = pokemon
                best = rarity
                closest = dist
            # Greedy for closest of same rarity
            elif rarity == best and dist < closest:
                pokemonBest = pokemon
                closest = dist
    if pokemonBest != None:
        
        if pokemonName != 'any':
            if pokemonName.upper() != str(pokedex[pokemonBest.pokemon_data.pokemon_id]).upper():
                pokemonBest = None
                logging.info("Couldn't find specific Pokemon @ this location.")
        else:
            logging.info(pokedex[pokemonBest.pokemon_data.pokemon_id] + " appears to be the rarest Pokemon @ location. Let's catch him!")
    else:
        data = [{
                'status': 'Did not find any pokemon @ given location.'
                }]
        json.dump(data, open('static/catch_data.json', 'w'))
        if firstTry == True:
            logging.info("Didn't find any, but sometimes this is a bug - let's retry.")
            pokemonBest = findBestPokemon(session,config,False,pokemonName)
        else:    
            logging.info("Sorry charlie, no Pokemon here. Enter a new location.")
        
   
    return pokemonBest


#Snipe!
def snipeABitch(session, pokemon, encounter, thresholdP=0.5, limit=10, delay=2):
    # Start encounter
    

    # Grab needed data from proto
    chances = encounter.capture_probability.capture_probability
    balls = encounter.capture_probability.pokeball_type
    bag = session.checkInventory().bag

    # Have we used a razz berry yet?
    berried = False

    # Make sure we aren't oer limit
    count = 0

    # Attempt catch
    while True:
        bestBall = items.UNKNOWN
        altBall = items.UNKNOWN
        #logging.info("Poke Balls: " + str(pokeBalls) + " Great Balls: " + str(greatBalls) + " Ultra Balls: " + str(ultraBalls))
        # Check for balls and see if we pass
        # wanted threshold
        logging.critical(balls)
        bag = session.checkInventory().bag
        
        ballTypes = {1:'Poke Ball',2:'Great Ball',3:'Ultra Ball'}
        for i in range(1,len(balls)+1):
            if i in bag and bag[i] > 0:
                if i == 1:
                    #PokeBalls
                    pokeBalls = bag[i]
                    logging.info("We have " + str(bag[i]) + " Poke Balls")
                    if chances[i] > thresholdP:
                        bestBall = i
                        break
                    else:
                        bestBall = i
                        altBall = i
                elif i == 2:
                    #GreatBalls
                    greatBalls = bag[i]
                    logging.info("We have " + str(bag[i]) + " Great Balls")
                    if float(chances[i]) > float(thresholdP):
                        bestBall = i
                        break
                    else:
                        if i-1 in bag and bag[i-1] > 0:
                            altBall = i-1
                            bestBall = i
                            
                elif i == 3:
                    #UltraBalls
                    ultraBalls = bag[i]
                    bestBall = i
                    logging.info("We have " + str(bag[i]) + " Ultra Balls")
                    if i-1 in bag and bag[i-1] > 0:
                        altBall = i-1
                        
                        
        if bestBall != items.UNKNOWN and altBall != items.UNKNOWN:
            logging.critical("Best ball: " + ballTypes[bestBall] + " Alt Ball: " + ballTypes[altBall])
        elif bestBall != items.UNKNOWN:
            logging.critical("Best ball: " + ballTypes[bestBall] + " Alt Ball: NONE!")
        # If we can't determine a ball, try a berry
        # or use a lower class ball
        if bestBall == items.UNKNOWN:
            if not berried and items.RAZZ_BERRY in bag and bag[items.RAZZ_BERRY]:
                logging.info("Using a RAZZ_BERRY")
                session.useItemCapture(items.RAZZ_BERRY, pokemon)
                berried = True
                time.sleep(delay)
                continue

            # if no alt ball, there are no balls
            elif altBall == items.UNKNOWN:
                data = [{
                'status': 'fail',
                'message': 'Out of usable balls'
                }]
                json.dump(data, open('static/catch_data.json', 'w'))
                time.sleep(1)
                raise GeneralPogoException("Out of usable balls")
                
            else:
                bestBall = altBall

        # Try to catch it!!
        logging.info("Using a %s" % items[bestBall])
        attempt = session.catchPokemon(pokemon, bestBall)
        time.sleep(delay)

        # Success or run away
        if attempt.status == 1:
            
            logging.critical("Congrats! We caught it!\n")
            return attempt
        if attempt.status == 2:
            logging.critical("Escaped ball, retry!")

        # CATCH_FLEE is bad news
        if attempt.status == 3:
            logging.info("Pokemon fled - possible soft ban.")
            return attempt

        # Only try up to x attempts
        count += 1
        if count >= limit:
            logging.info("Over catch limit")
            return None




# Do Inventory stuff
def getInventory(session):
    logging.info("Get Inventory:")
    logging.info(session.getInventory())


def doSnipe(session,config,snipeLoc,pokemonName):
    if pokemonName == "":
        pokemonName = 'any'
    if session:
	
        
        # Things we need GPS for
        if config.get('CONFIG','startLoc'):
			#Set up home location
            prevLatitude, prevLongitude, _ = session.getCoordinates()
            snipeLocSplit = snipeLoc.split(",")
            #Set up snipe location
            snipeLatitude = float(snipeLocSplit[0])
            snipeLongitude = float(snipeLocSplit[1])

			
			#move to snipe location
            session.setCoordinates(snipeLatitude,snipeLongitude)
			
			#Search snipe location for most powerful pokemon
            pokeMon = findBestPokemon(session,config,True,pokemonName)
            
            if pokeMon == None:
                session.setCoordinates(prevLatitude,prevLongitude)
                render_template("result.html")
                return
			
			#Encounter pokemon
            remoteEncounter = session.encounterPokemon(pokeMon)
            			
			#move back home to capture
            session.setCoordinates(prevLatitude,prevLongitude)
            logging.info("Encountered pokemon - moving back to start location to catch.")
			#Wait for move to complete
            logging.info('Ignore CP: ' + str(ignoreCP))
            time.sleep(2)
            if ignoreCP == False:
            
                if int(remoteEncounter.wild_pokemon.pokemon_data.cp) < int(minCP):
                    data = [{
                    'status': 'fail',
                    'message': 'Did not attempt to catch ' +  pokedex[remoteEncounter.wild_pokemon.pokemon_data.pokemon_id] + ': CP of ' + str(remoteEncounter.wild_pokemon.pokemon_data.cp)  + ' did not meet threshold of ' + str(minCP) + '.'
                    }]
                        
                    json.dump(data, open('static/catch_data.json', 'w'))
                    logging.critical('Did not attempt to catch ' +  pokedex[remoteEncounter.wild_pokemon.pokemon_data.pokemon_id] + ': CP of ' + str(remoteEncounter.wild_pokemon.pokemon_data.cp)  + ' did not meet threshold of ' + str(minCP) + '.')
                    return
                
            snipe = snipeABitch(session, pokeMon, remoteEncounter)
            if snipe.status == 3:
                data = [{
                'status': 'fail',
                'message': 'Pokemon fled'
                }]
                        
                json.dump(data, open('static/catch_data.json', 'w'))
                
            if snipe.status != 3:
                logging.info("Heres what we caught:\n")
                for pokez in session.getInventory().party:
                    if pokez.id == snipe.captured_pokemon_id:
                        logging.info(pokez)
                        
                        data = [{
                        'status': 'Success. Caught a ' + pokedex[pokez.pokemon_id] + ' CP:' + str(pokez.cp),
                        'pokemon_name': pokedex[pokez.pokemon_id],
                        'pokemon_id': pokez.pokemon_id

                               }]
                        json.dump(data, open('static/catch_data.json', 'w'))
                        time.sleep(1)
          
    else:
        logging.critical('Session not created successfully')

		
if __name__ == '__main__':
    global ignoreCP 
    ignoreCP = False
    data = [{'status':'Server startup. Nothing to report.'}]
    json.dump(data, open('static/catch_data.json', 'w'))
    time.sleep(1)
    setupLogger()
    logging.debug('Logger set up')

    	
	#parse in configuration from config.ini
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    #config.get('AUTH','type')
    #config.get('AUTH','username')
    #config.get('AUTH','password')
    #config.get('CONFIG','startLoc')
    #config.get('CONFIG','minCP')
    
    # Check service
    minCP = int(config.get('CONFIG','minCP'))
    if config.get('AUTH','type') not in ['ptc', 'google']:
        logging.error('Invalid auth service {}'.format(config.get('AUTH','type')))
        sys.exit(-1)

    # Create PokoAuthObject
    poko_session = PokeAuthSession(
        config.get('AUTH','username'),
        config.get('AUTH','password'),
        config.get('AUTH','type'),
        ''.join(['encrypt/',config.get('CONFIG', 'encryptFile')]),
        geo_key=""
    )

    # Authenticate with a given location
    # Location is not inherent in authentication
    # But is important to session
    if config.get('CONFIG','startLoc'):
        session = poko_session.authenticate(locationLookup=config.get('CONFIG','startLoc'))
    else:
        session = poko_session.authenticate()

    # Time to show off what we can do
    logging.info("Successfully logged in to Pokemon Go! Starting web server on port 5100.")
    
    app.run(host='0.0.0.0', port=5100, debug=True)
    url_for('static', filename='catch_data.json')
    	
    
	
