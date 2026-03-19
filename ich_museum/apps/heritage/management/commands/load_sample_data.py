"""Load sample heritage items for development/demo."""
from django.core.management.base import BaseCommand
from apps.accounts.models import User
from apps.heritage.models import Category, Region, Inheritor, HeritageItem, ItemStatus


REGIONS = [
    ('北京', 'Beijing'), ('江苏', 'Jiangsu'), ('浙江', 'Zhejiang'),
    ('广东', 'Guangdong'), ('四川', 'Sichuan'), ('陕西', 'Shaanxi'),
    ('福建', 'Fujian'), ('云南', 'Yunnan'),
]

SAMPLE_ITEMS = [
    {
        'name': '格萨尔',
        'name_en': 'Epic of King Gesar',
        'category_code': 'folk_literature',
        'region': '四川',
        'summary': '《格萨尔》是藏族人民集体创作的一部伟大的英雄史诗，是世界上最长的史诗之一。',
        'summary_en': 'The Epic of King Gesar is a heroic epic collectively created by the Tibetan people, one of the longest epics in the world.',
        'description': '# 格萨尔\n\n《格萨尔》是一部篇幅宏大的藏族民间说唱体英雄史诗，讲述了格萨尔王降伏妖魔、抑强扶弱、统一各部落的英雄故事。\n\n## 艺术特色\n\n- 说唱结合的表演形式\n- 韵散交替的文学结构\n- 丰富的神话色彩\n- 活态传承，至今仍有艺人说唱\n\n## 传承方式\n\n格萨尔的传承主要依靠民间说唱艺人，他们被称为"仲肯"，能够背诵数十万行诗句。',
        'history': '《格萨尔》产生于藏族氏族社会开始瓦解、奴隶制国家政权逐渐形成的历史时期。2009年被列入联合国教科文组织非物质文化遗产名录。',
    },
    {
        'name': '京剧',
        'name_en': 'Peking Opera',
        'category_code': 'traditional_opera',
        'region': '北京',
        'summary': '京剧是中国五大戏曲剧种之一，被视为中国国粹，位列中国戏曲三鼎甲"榜首"。',
        'summary_en': 'Peking Opera is one of the five major opera genres in China, regarded as the quintessence of Chinese culture.',
        'description': '# 京剧\n\n京剧，又称平剧、京戏，是中国影响最大的戏曲剧种，分布地以北京为中心，遍及全国各地。\n\n## 历史渊源\n\n清代乾隆五十五年（1790年）起，原在南方演出的三庆、四喜、春台、和春四大徽班陆续进入北京，与来自湖北的汉调艺人合作，同时接受了昆曲、秦腔的部分剧目、曲调和表演方法，又吸收了一些地方民间曲调，通过不断的交流、融合，最终形成京剧。\n\n## 艺术特色\n\n京剧表演的四种艺术手法：唱、念、做、打，也是京剧表演四项基本功。',
        'history': '京剧前身是清初流行于江南地区的徽班，通过不断吸收其他剧种的优点，逐渐发展成为中国最大的戏曲剧种。2010年被列入联合国教科文组织非物质文化遗产名录。',
    },
    {
        'name': '昆曲',
        'name_en': 'Kunqu Opera',
        'category_code': 'traditional_opera',
        'region': '江苏',
        'summary': '昆曲是中国最古老的剧种之一，被誉为"百戏之祖"，2001年被联合国教科文组织列为首批"人类口头和非物质遗产代表作"。',
        'summary_en': 'Kunqu Opera is one of the oldest opera forms in China, known as the "ancestor of all operas".',
        'description': '# 昆曲\n\n昆曲，原名"昆山腔"或简称"昆腔"，是中国古老的戏曲声腔、剧种，现又被称为"昆剧"。\n\n## 艺术特色\n\n昆曲以鼓、板控制演唱节奏，以曲笛、三弦等为主要伴奏乐器，其唱念语音为"中州韵"。昆曲的表演，也有它独特的体系、风格，它最大的特点是抒情性强、动作细腻，歌唱与舞蹈的身段结合得巧妙而和谐。',
        'history': '昆曲发源于14世纪中国的苏州昆山，后经魏良辅等人的改良而走向全国。',
    },
]

SAMPLE_ITEMS += [
    {
        'name': '秧歌',
        'name_en': 'Yangge Dance',
        'category_code': 'traditional_dance',
        'region': '陕西',
        'summary': '秧歌是中国北方地区广泛流传的一种极具群众性和代表性的民间舞蹈，历史悠久，风格多样。',
        'summary_en': 'Yangge is a popular folk dance widely spread in northern China with a long history and diverse styles.',
        'description': '# 秧歌\n\n秧歌是中国北方最具代表性的民间舞蹈之一，以其欢快热烈的表演风格深受群众喜爱。\n\n## 主要流派\n\n- **陕北秧歌** — 粗犷奔放，气势磅礴\n- **东北秧歌** — 泼辣火爆，幽默风趣\n- **山东秧歌** — 刚劲有力，舒展大方\n- **河北秧歌** — 轻盈活泼，灵巧多变\n\n## 表演形式\n\n秧歌通常在春节、元宵节等传统节日期间表演，表演者手持扇子、手帕、彩绸等道具，伴随着锣鼓声翩翩起舞。',
        'history': '秧歌起源于农业劳动，最早可追溯到宋代。2006年被列入第一批国家级非物质文化遗产名录。',
    },
    {
        'name': '苏州评弹',
        'name_en': 'Suzhou Pingtan',
        'category_code': 'quyi',
        'region': '江苏',
        'summary': '苏州评弹是苏州评话和苏州弹词的总称，是采用吴语徒口讲说表演的传统曲艺说书形式。',
        'summary_en': 'Suzhou Pingtan is a traditional storytelling art form performed in the Wu dialect, combining spoken narrative with musical accompaniment.',
        'description': '# 苏州评弹\n\n苏州评弹是一门古老的说唱艺术，以其优美的唱腔、细腻的表演和丰富的文学内涵著称。\n\n## 两大形式\n\n- **评话** — 只说不唱，以一人说表为主\n- **弹词** — 有说有唱，以三弦、琵琶伴奏\n\n## 艺术特色\n\n- 使用苏州方言表演\n- 唱腔婉转优美，有"中国最美声音"之誉\n- 一人多角，表演细腻传神\n- 书目丰富，涵盖历史、武侠、言情等题材',
        'history': '苏州评弹起源于明末清初，至今已有400多年历史。2006年被列入第一批国家级非物质文化遗产名录。',
    },
    {
        'name': '中国剪纸',
        'name_en': 'Chinese Paper Cutting',
        'category_code': 'fine_arts',
        'region': '陕西',
        'summary': '中国剪纸是用剪刀或刻刀在纸上剪刻花纹，用于装点生活或配合其他民俗活动的一种民间艺术。',
        'summary_en': 'Chinese paper cutting is a folk art of cutting patterns on paper with scissors or knives.',
        'description': '# 中国剪纸\n\n剪纸艺术是最古老的中国民间艺术之一，作为一种镂空艺术，它能给人以视觉上以透空的感觉和艺术享受。\n\n## 主要流派\n\n- **陕北剪纸**：粗犷豪放，造型简练\n- **江南剪纸**：精巧秀丽，玲珑剔透\n- **山东剪纸**：线条流畅，装饰性强',
        'history': '剪纸在中国有着悠久的历史，可追溯到公元6世纪。2009年入选联合国教科文组织非物质文化遗产名录。',
    },
    {
        'name': '中国书法',
        'name_en': 'Chinese Calligraphy',
        'category_code': 'fine_arts',
        'region': '北京',
        'summary': '中国书法是以笔、墨、纸等为主要工具材料，通过汉字书写来表达情感和审美的艺术形式。',
        'summary_en': 'Chinese calligraphy is an art form expressing emotions and aesthetics through the writing of Chinese characters.',
        'description': '# 中国书法\n\n中国书法是一门古老的汉字书写艺术，从甲骨文、石鼓文、金文演变而为大篆、小篆、隶书，至定型于东汉、魏、晋的草书、楷书、行书等。\n\n## 五大书体\n\n1. **篆书** — 最古老的书体\n2. **隶书** — 汉代主要书体\n3. **楷书** — 标准书体\n4. **行书** — 介于楷书和草书之间\n5. **草书** — 最为奔放的书体',
        'history': '中国书法的历史可追溯到商代甲骨文，已有三千多年的历史。2009年入选联合国教科文组织非物质文化遗产名录。',
    },
    {
        'name': '太极拳',
        'name_en': 'Tai Chi Chuan',
        'category_code': 'sports_acrobatics',
        'region': '北京',
        'summary': '太极拳是以中国传统儒、道哲学中的太极、阴阳辩证理念为核心思想，集颐养性情、强身健体、技击对抗等多种功能为一体的传统拳术。',
        'summary_en': 'Tai Chi Chuan is a traditional Chinese martial art combining health cultivation, self-defense, and philosophical principles.',
        'description': '# 太极拳\n\n太极拳，国家级非物质文化遗产，是以中国传统儒、道哲学中的太极、阴阳辩证理念为核心思想的传统拳术。\n\n## 主要流派\n\n- **陈式太极拳** — 最古老的流派\n- **杨式太极拳** — 流传最广\n- **武式太极拳** — 小巧紧凑\n- **吴式太极拳** — 柔化为主\n- **孙式太极拳** — 融合形意、八卦',
        'history': '太极拳起源于17世纪中叶的河南温县陈家沟。2020年被列入联合国教科文组织非物质文化遗产名录。',
    },
    {
        'name': '中医针灸',
        'name_en': 'Acupuncture and Moxibustion',
        'category_code': 'traditional_medicine',
        'region': '北京',
        'summary': '针灸是中医学的重要组成部分，通过经络、腧穴的传导作用，运用一定的操作法来治疗全身疾病。',
        'summary_en': 'Acupuncture and moxibustion is an important part of traditional Chinese medicine for treating diseases.',
        'description': '# 中医针灸\n\n针灸由"针"和"灸"构成，是东方医学的重要组成部分之一。\n\n## 基本原理\n\n针灸疗法的基本原理是通过刺激人体特定的穴位，调节经络气血的运行，从而达到治疗疾病的目的。\n\n## 主要技法\n\n- **毫针刺法** — 最常用的针刺方法\n- **艾灸** — 用艾叶制成的艾条或艾柱熏烤穴位\n- **拔罐** — 利用负压吸附于体表',
        'history': '针灸起源于中国，有着2000多年的历史。2010年被列入联合国教科文组织非物质文化遗产名录。',
    },
]

SAMPLE_ITEMS += [
    {
        'name': '景德镇手工制瓷技艺',
        'name_en': 'Jingdezhen Porcelain Making',
        'category_code': 'craftsmanship',
        'region': '江苏',
        'summary': '景德镇手工制瓷技艺是景德镇传统的制瓷手工技艺，包括拉坯、利坯、画坯、施釉和烧窑等工序。',
        'summary_en': 'Jingdezhen porcelain making is the traditional handcraft technique of porcelain production.',
        'description': '# 景德镇手工制瓷技艺\n\n景德镇制瓷历史悠久，瓷器造型优美、品种繁多、装饰丰富、风格独特，以"白如玉，明如镜，薄如纸，声如磬"著称。\n\n## 主要工序\n\n1. **练泥** — 将瓷石加工成瓷泥\n2. **拉坯** — 在转盘上拉制成型\n3. **印坯** — 用模具印制\n4. **利坯** — 修整坯体\n5. **画坯** — 绑定装饰图案\n6. **施釉** — 上釉\n7. **烧窑** — 高温烧制',
        'history': '景德镇制瓷始于汉代，至今已有2000多年历史。2006年被列入第一批国家级非物质文化遗产名录。',
    },
    {
        'name': '古琴艺术',
        'name_en': 'Guqin Art',
        'category_code': 'traditional_music',
        'region': '北京',
        'summary': '古琴是中国最古老的弹拨乐器之一，有三千多年的历史，被誉为"琴棋书画"四艺之首。',
        'summary_en': 'Guqin is one of the oldest plucked string instruments in China with over 3,000 years of history.',
        'description': '# 古琴艺术\n\n古琴，又称瑶琴、玉琴、七弦琴，是中国传统拨弦乐器，有三千年以上历史。\n\n## 艺术特色\n\n古琴音域宽广，音色深沉，余音悠远。古琴的演奏技法丰富，包括散音、泛音、按音三种基本音色。\n\n## 代表曲目\n\n- 《高山流水》\n- 《广陵散》\n- 《平沙落雁》\n- 《梅花三弄》',
        'history': '古琴是中国最早的弹弦乐器，2003年被联合国教科文组织列为"人类口头和非物质遗产代表作"。',
    },
    {
        'name': '川剧变脸',
        'name_en': 'Sichuan Opera Face Changing',
        'category_code': 'traditional_opera',
        'region': '四川',
        'summary': '变脸是川剧表演的特技之一，用于揭示剧中人物的内心及思想感情的变化。',
        'summary_en': 'Face changing is a special technique in Sichuan Opera used to reveal characters\' inner emotions.',
        'description': '# 川剧变脸\n\n变脸是运用在川剧艺术中塑造人物的一种特技，属于揭示剧中人物内心思想感情的一种浪漫主义手法。\n\n## 变脸方法\n\n- **抹脸** — 将化妆油彩涂在脸的某一特定部位上\n- **吹脸** — 利用吹粉的方式变脸\n- **扯脸** — 事前将脸谱画在一张张绸子上，表演时一张一张地将它扯下来',
        'history': '川剧变脸起源于清代，已有300多年历史。变脸技艺被列为国家二级机密。',
    },
    {
        'name': '妈祖信俗',
        'name_en': 'Mazu Belief and Customs',
        'category_code': 'folk_customs',
        'region': '福建',
        'summary': '妈祖信俗是以崇奉和颂扬妈祖的立德、行善、大爱精神为核心，以妈祖宫庙为主要活动场所的民俗文化。',
        'summary_en': 'Mazu belief and customs is a folk culture centered on the worship of Mazu, the goddess of the sea.',
        'description': '# 妈祖信俗\n\n妈祖信俗是源于对妈祖的崇拜而逐渐形成的一种民间信俗，是中国最具影响力的航海保护神信仰。\n\n## 主要活动\n\n- **妈祖祭典** — 每年农历三月廿三妈祖诞辰\n- **妈祖巡安** — 妈祖神像出巡\n- **妈祖回娘家** — 分灵妈祖回祖庙谒祖',
        'history': '妈祖信俗起源于宋代福建莆田湄洲岛，已有千年历史。2009年被列入联合国教科文组织非物质文化遗产名录。',
    },
]


class Command(BaseCommand):
    help = '加载非遗项目示例数据'

    def handle(self, *args, **options):
        # Get or create admin user as content creator
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            self.stderr.write('请先创建 superuser: python manage.py createsuperuser')
            return

        # Create regions
        region_map = {}
        for name, name_en in REGIONS:
            region, _ = Region.objects.get_or_create(name=name, defaults={'name_en': name_en})
            region_map[name] = region

        created = 0
        for item_data in SAMPLE_ITEMS:
            if HeritageItem.objects.filter(name=item_data['name']).exists():
                self.stdout.write(f'  跳过（已存在）: {item_data["name"]}')
                continue

            category = Category.objects.get(code=item_data['category_code'])
            region = region_map.get(item_data.get('region'))

            HeritageItem.objects.create(
                name=item_data['name'],
                name_en=item_data.get('name_en', ''),
                category=category,
                region=region,
                summary=item_data['summary'],
                summary_en=item_data.get('summary_en', ''),
                description=item_data['description'],
                history=item_data.get('history', ''),
                status=ItemStatus.PUBLISHED,
                created_by=admin,
            )
            created += 1
            self.stdout.write(f'  ✅ {item_data["name"]}')

        self.stdout.write(self.style.SUCCESS(f'\n完成！新增 {created} 个非遗项目'))
