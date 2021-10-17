import random, requests, re
from time import sleep as s
from apis import pushshift_api, reddit_api
from utils import chance
from .utils import get_subreddit, AVOID_WORDS
from config.reddit_config import CONFIG
from config.reddit.reddit_sub_lists import CROSSPOST_SUBS
from logs.logger import log
from praw.exceptions import APIException

wordgroup = [['last','recent'],['in','by','at'],['looking at','watching'],['took','attended'],['arrives','comes'],['approach','procedure'],['order','buy','purchase'],['recommended','suggested','endorsed','proposed'],['approved','accepted'],['employees','workers'],['amazing','incredible','unbelievable','wonderful','fantastic','extraordinary'],['anger','enrage','infuriate'],['angry','mad','furious','enraged'],['answer','reply','response'],['ask','question','request','query'],['awful','dreadful','terrible','abominable','bad','poor','unpleasant'],['rotten','contaminated','spoiled','tainted'],['faulty','improper','inappropriate','unsuitable','disagreeable','unpleasant'],['bad','evil','immoral','wicked','corrupt','harmful','deplorable','gross','heinous','obnoxious','despicable'],['beautiful','pretty','lovely','handsome','attractive','gorgeous','dazzling','splendid','magnificent','comely','fair','ravishing','graceful','elegant','fine','exquisite','aesthetic','pleasing','shapely','delicate','stunning','glorious','heavenly','resplendent','radiant','glowing','blooming','sparkling'],['begin','start','open','launch','initiate','commence','inaugurate','originate'],['big','enormous','huge','immense','gigantic','vast','colossal','gargantuan','large','sizable','grand','great','tall','substantial','mammoth','astronomical','ample','broad','expansive','spacious','stout','tremendous','titanic','mountainous'],['brave','courageous','fearless','dauntless','intrepid','plucky','daring','heroic','valorous','audacious','bold','gallant','valiant','doughty','mettlesome'],['break','fracture','rupture','shatter','smash','wreck','crash','demolish'],['bright','shiny','intellectual'],['calm','quiet','peaceful','still','collected'],['come','approach'],['cool','cold','frosty','icy'],['crooked','bent','twisted','curved','hooked'],['shout','yell','scream'],['cry','sob'],['cut','slice','slit','chop','crop'],['dangerous','risky','unsafe'],['dark','shadowy','dim','shaded'],['decide','determine','settle','choose','resolve'],['definite','certain','sure','positive','determined','clear','distinct','obvious'],['delicious','appetizing','scrumptious','delightful','enjoyable','toothsome','exquisite'],['describe','portray','characterize','picture','narrate','relate','recount','represent','report','record'],['destroy','ruin','demolish','kill','slay'],['difference','disagreement','inequity','contrast','dissimilarity','incompatibility'],['do','execute','finish','conclude','accomplish','achieve','attain'],['boring','tiring','tiresome','uninteresting'],['slow','dumb','stupid','unimaginative'],['eager','enthusiastic','involve','interest'],['enjoy','appreciate','like'],['explain','elaborate','clarify','define','interpret','justify','account for'],['fair','unbiased','objective','unprejudiced','honest'],['fall','drop','descend','tumble'],['false','untrue','deceptive','fallacious'],['famous','well-known','celebrated','famed','illustrious','distinguished','noted','notorious'],['fast','quick','rapid','speedy','hasty'],['fat','corpulent','beefy','plump','chubby','chunky','bulky'],['fear','anxiety','panic'],['funny','humorous','amusing','comical','laughable'],['get','acquire','obtain','secure','gather'],['go','recede','depart','fade','disappear','move','travel','proceed'],['good','excellent','fine','superior','marvelous','suitable','proper','pleasant','satisfactory','reliable','helpful','valid','genuine','great','respectable','edifying'],['great','noteworthy','worthy','distinguished','remarkable','grand','considerable','powerful','much','mighty'],['gross','rude','vulgar'],['happy','pleased','contented','satisfied','joyful','cheerful','glad','blissful'],['hate','despise','disfavor','dislike'],['have','possess','own'],['help','aid','assist','support','encourage'],['hide','cover'],['hurry','rush','run','speed','race','hasten','urge','accelerate','bustle'],['hurt','damage','harm','injure','wound','pain'],['idea','thought','concept','conception','plan'],['important','necessary','vital','critical','indispensable','valuable','essential','significant'],['interesting','fascinating','engaging','thought-provoking','curious','appealing'],['keep','hold','retain','withhold','preserve','maintain','sustain'],['kill','slay','execute','assassinate','murder','destroy','abolish'],['lazy','inactive','sluggish'],['little','tiny','small','petite'],['look','gaze','see','glance','watch','peek','stare','observe','view','spy','sight','discover','notice','recognize','peer','eye'],['love','like','admire','esteem','fancy','care for','cherish','adore','treasure','worship','appreciate','savor'],['make','create','form','construct','design','fabricate','manufacture','produce','develop','do','execute','compose','perform','acquire'],['mark','label','tag','price','ticket','sign','note','notice'],['mischievous','prankish','playful'],['move','go','walk','jog','run','sprint','hurry','wander','roam'],['moody','temperamental','short-tempered'],['neat','clean','orderly','elegant','well-organized','super','desirable','well-kept','shapely'],['new','fresh','modern','recent'],['old','ancient','aged','used','worn','faded','broken-down','old-fashioned'],['part','portion','share','piece','allotment','section','fraction','fragment'],['place','area','spot','region','location','position','residence','set','state'],['plan','plot','scheme','design','map','diagram','procedure','arrangement','intention','device','contrivance','method','way','blueprint'],['popular','well-liked','celebrate','common'],['predicament','quandary','dilemma','problem'],['put','place','set','attach','set aside','effect','achieve','do'],['quiet','silent','still','soundless','mute','peaceful','calm','restful'],['right','correct','good','honest','moral','proper','suitable'],['run','race','hurry','sprint','rush'],['say','tell','inform','notify','advise','narrate','explain','reveal','disclose','remark','converse','speak','affirm','suppose','utter','negate','express','verbalize','articulate','pronounce','convey','impart','state','announce'],['scared','afraid','frightened','terrified','fearful','worried','horrified','shocked'],['show','display','present','note','reveal','demonstrate'],['slow','unhurried','tedious'],['stop','end','finish','quit'],['story','myth','legend','fable','narrative','chronicle','anecdote','memoir'],['strange','odd','unusual','unfamiliar','uncommon','weird','outlandish','curious','unique','exclusive','irregular'],['remove','steal','lift','rob',],['purchase','buy'],['tell','disclose','reveal','narrate','talk','explain'],['think','reflect'],['trouble','disaster','misfortune','inconvenience'],['true','accurate','right','proper','precise','exact','valid','genuine'],['ugly','unpleasant','terrifying','gross','unsightly'],['unhappy','miserable','uncomfortable','unfortunate','depressed','sad'],['use','utilize'],['wrong','incorrect','inaccurate','mistaken'],['know','acknowledge','recognise','recognize'],['people','citizenry','masses','mass'],['now','forthwith','nowadays','instantly'],['first','beginning','initiatory','initiative','firstly'],]

def find_synonyms(keyword):
    keyword=keyword.lower()
    for sub_list in wordgroup:
        if keyword in sub_list:
            while True:
                word = random.choice(sub_list)
                if word != keyword:
                    # print('found "'+keyword+'"; chosen synonym "'+word+'"')
                    return word

title_chars=['!','.',';','?']
invisible_chars = ['‍      ','   ‏‏‎   ','‏‏‎‏‏‎‏‏‎‏‏‎­',' ⠀']

def edit_text(var, mode):
    if mode == 'body':
        mychars=[]
        if ' ' in var:
            for index, x in enumerate(var):
                if x == ' ':mychars.append(index)
            editedtext = list(var)
            editedtext[random.choice(mychars)] = random.choice(invisible_chars)
            editedtext = ''.join(editedtext)
            for x in editedtext.split():
                synonym=find_synonyms(x)
                if synonym != None:
                    words = editedtext.split()
                    words[words.index(x)] = synonym
                    editedtext = " ".join(words)
                    return editedtext
        else:return var
    elif mode == 'title':
        if any(not c.isalnum() for c in var[-2:]):return var.replace(var[-2:], var[-2]+' '+random.choice(title_chars))
        else:return var+random.choice(title_chars)

class Posts():
  def __init__(self):
    self.psapi = pushshift_api
    self.rapi = reddit_api

  def get_post(self, subreddit=None):
    log.info(f"finding a post to re-post")    
    got_post = False
    attempts = 0
    while not got_post:
      # use the supplied subreddit
      # otherwise choose one randomly
      if subreddit:
        log.info(f"searching post in sub: {subreddit}")
        sub = self.rapi.subreddit(subreddit)
      else:
        # if there are subreddits in the subreddit list pull randomly from that
        # otherwise pull a totally random subreddit
        sub = self.rapi.subreddit(random.choice(CONFIG['reddit_sub_list'])) if CONFIG['reddit_sub_list'] else get_subreddit(getsubclass=True)
          
        log.info(f"searching post in sub: {sub.display_name}")
      try:
        post_id = self.psapi.get_posts(sub.display_name)[0]['id']
        # don't use posts that have avoid words in title
        if not any(word in comment.body for word in AVOID_WORDS):
          got_post = True
      except Exception as e:
        log.info(f"couldn't find post in {sub}")
        # sub = self.rapi.random_subreddit(nsfw=False)
        # log.info(f"trying in: {subreddit}")
        attempts += 1
        log.info(f"repost attempts: {attempts}")
        if attempts > 3:
          log.info(f"couldn't find any posts - skipping reposting for now")
          return

    return self.rapi.submission(id=post_id)

  def crosspost(self, subreddit):
    for idx, subs in enumerate(CROSSPOST_SUBS):
      if subs[0] == subreddit:
        return random.choice(subs[idx])

  # why do my eyes hurt
  def repost(self, roll=1, subreddit=None):
    if chance(roll):
      log.info("running repost")
      # log.info("running _repost")
      post = self.get_post(subreddit=subreddit)
      if not post: return
      api_call=requests.get(post.url).status_code
      if api_call != 200:
        if api_call == 429:
          print('too many requests to pushshift')
          s(random.uniform(3,8))
        else:
          print('pushshift http error: '+str(api_call))
        return
      else:
        log.info(f"reposting post: {post.id}")
        
        if post.is_self:
          if post.selftext not in ('[removed]','[deleted]') and bool(re.findall(r'20[0-9][0-9]|v.redd.it', post.selftext)) == False:
            params = {"title": edit_text(post.title, 'title'), "selftext": edit_text(post.selftext, 'body')}
          else:
            print('Info: skipping post; it was malformed or date indicated')
            # print(post.selftext)
        else:params = {"title": edit_text(post.title, 'title'), "url": post.url}

        sub = post.subreddit

        # randomly choose a potential subreddit to cross post
        if CONFIG['reddit_crosspost_enabled']:
          sub = self.rapi.subreddit(self.crosspost(sub.display_name))
        try:
          self.rapi.subreddit(sub.display_name).submit(**params)
          return
        except (UnboundLocalError, TypeError):pass
        except APIException as e:
          log.info(f"REPOST ERROR: {e}")
          return
    else:
      pass
      # log.info("not running repost")
      # log.info("not running _repost")


## to do: add flairs compability or a way to avoid flairs
