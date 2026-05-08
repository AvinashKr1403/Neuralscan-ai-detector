from flask import Flask, request, jsonify, render_template
try:
    from flask_cors import CORS
    has_cors = True
except ImportError:
    has_cors = False

import pickle, os, re, math
from collections import Counter

app = Flask(__name__)
if has_cors:
    CORS(app)

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import cross_val_score
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

DATASET = [
    ("Furthermore, it is important to note that artificial intelligence plays a crucial role in modern technological advancement. Leveraging these comprehensive solutions enables robust paradigm shifts across multiple domains.", "ai"),
    ("In conclusion, the utilization of machine learning algorithms provides substantial benefits. It is worth noting that these systems demonstrate remarkable capabilities in data processing and analysis.", "ai"),
    ("Additionally, as mentioned in previous studies, the implementation of neural networks offers a comprehensive framework for understanding complex patterns. With that said, these methodologies are certainly worth exploring.", "ai"),
    ("The multifaceted nature of this phenomenon necessitates a holistic approach. Furthermore, the intricate interplay of various factors contributes to the overall complexity of the situation.", "ai"),
    ("It should be noted that climate change represents one of the most significant challenges facing humanity. Robust mitigation strategies are absolutely essential for addressing this critical issue comprehensively.", "ai"),
    ("In this context, it is worth noting that economic development and environmental sustainability are not mutually exclusive goals. Leveraging innovative technologies can facilitate the achievement of both objectives simultaneously.", "ai"),
    ("The comprehensive analysis reveals that productivity metrics demonstrate consistent improvement when collaborative frameworks are properly implemented. This paradigm shift reflects broader organizational transformation.", "ai"),
    ("As a result of these developments, it becomes increasingly clear that digital transformation is not merely a technological imperative but a fundamental business necessity in today's competitive landscape.", "ai"),
    ("Furthermore, the proliferation of data-driven decision-making processes has fundamentally altered the operational dynamics of modern enterprises. Robust analytics capabilities are therefore paramount.", "ai"),
    ("It is important to understand that the convergence of various technological trends creates unprecedented opportunities for innovation and growth across diverse industry sectors and geographical regions.", "ai"),
    ("The synthesis of available evidence suggests that multimodal learning approaches yield superior outcomes compared to traditional pedagogical methodologies. Comprehensive implementation strategies must therefore be developed.", "ai"),
    ("Certainly, the strategic alignment of organizational objectives with technological capabilities represents a cornerstone of successful digital transformation initiatives in contemporary business environments.", "ai"),
    ("Of course, stakeholder engagement plays a pivotal role in ensuring the successful implementation of transformative initiatives. Comprehensive communication strategies are therefore absolutely essential for organizational success.", "ai"),
    ("The empirical evidence unequivocally demonstrates that proactive risk management frameworks significantly enhance organizational resilience. Leveraging data analytics capabilities provides robust insights for decision-making processes.", "ai"),
    ("In summary, the intersection of artificial intelligence and healthcare presents remarkable opportunities for improving patient outcomes. These comprehensive solutions leverage advanced algorithms to deliver personalized medical interventions.", "ai"),
    ("The paradigmatic shift toward remote work environments has necessitated the development of more sophisticated digital collaboration tools. Furthermore, these platforms must address diverse user needs comprehensively.", "ai"),
    ("It is worth emphasizing that sustainable development goals require the coordinated effort of multiple stakeholders. Robust international cooperation frameworks are absolutely essential for achieving meaningful progress.", "ai"),
    ("Additionally, the optimization of supply chain operations through advanced analytics and machine learning technologies yields significant competitive advantages. These comprehensive methodologies fundamentally transform operational efficiency.", "ai"),
    ("The utilization of blockchain technology in financial services represents a paradigmatic evolution in transaction processing. Furthermore, these decentralized systems provide robust security mechanisms for digital assets.", "ai"),
    ("In conclusion, the integration of renewable energy sources into existing power grids presents both technical challenges and significant opportunities. Leveraging innovative solutions is certainly crucial for successful implementation.", "ai"),
    ("The comprehensive examination of epidemiological data reveals significant correlations between socioeconomic factors and health outcomes. It is worth noting that these disparities necessitate targeted policy interventions.", "ai"),
    ("Furthermore, advancements in genomic research have substantially enhanced our understanding of complex disease mechanisms. These groundbreaking discoveries offer unprecedented opportunities for personalized therapeutic approaches.", "ai"),
    ("It is important to acknowledge that mental health conditions represent a significant public health challenge. Comprehensive, evidence-based interventions are absolutely essential for addressing this multifaceted issue effectively.", "ai"),
    ("The implementation of precision medicine strategies requires robust integration of diverse data sources. Additionally, sophisticated analytical frameworks are necessary to extract meaningful insights from complex biological datasets.", "ai"),
    ("As evidenced by numerous studies, regular physical activity yields substantial benefits across multiple dimensions of health. Leveraging behavioral science principles can facilitate more effective health promotion campaigns.", "ai"),
    ("In this context, the development of novel therapeutic modalities represents a significant scientific achievement. These comprehensive approaches utilize cutting-edge biotechnological innovations to address previously intractable conditions.", "ai"),
    ("The holistic assessment of nutritional interventions requires consideration of multiple variables including macronutrient composition, micronutrient availability, and individual metabolic characteristics.", "ai"),
    ("Furthermore, the establishment of robust clinical trial protocols is absolutely essential for generating reliable evidence regarding treatment efficacy. Rigorous methodological standards must therefore be maintained throughout.", "ai"),
    ("It should be noted that the global burden of chronic diseases continues to escalate at an alarming rate. Comprehensive prevention strategies leveraging innovative technologies offer promising pathways toward mitigation.", "ai"),
    ("The synthesis of current scientific literature suggests that mindfulness-based interventions demonstrate significant efficacy in reducing psychological distress. These evidence-based approaches warrant broader clinical implementation.", "ai"),
    ("The implementation of competency-based educational frameworks represents a significant paradigm shift in pedagogical approaches. Furthermore, these comprehensive methodologies facilitate more personalized learning experiences.", "ai"),
    ("It is important to recognize that educational equity requires systemic intervention across multiple dimensions. Leveraging technology-enhanced learning environments can facilitate broader access to quality educational opportunities.", "ai"),
    ("In conclusion, the integration of social-emotional learning components into academic curricula yields substantial benefits for student development. These comprehensive approaches address the multifaceted nature of education effectively.", "ai"),
    ("Additionally, the utilization of formative assessment strategies provides educators with robust feedback mechanisms. It is worth noting that these data-driven approaches facilitate more responsive instructional practices.", "ai"),
    ("The evidence-based examination of educational interventions reveals that differentiated instruction significantly enhances learning outcomes. Certainly, these comprehensive approaches must be thoughtfully implemented to maximize effectiveness.", "ai"),
    ("Furthermore, professional development opportunities for educators play a crucial role in maintaining high pedagogical standards. Robust training programs are therefore absolutely essential for continuous improvement.", "ai"),
    ("It should be noted that early childhood education represents a foundational investment in human capital development. Comprehensive early intervention programs leverage critical developmental windows to maximize long-term outcomes.", "ai"),
    ("The paradigm of collaborative learning environments has demonstrated remarkable efficacy in fostering both academic achievement and interpersonal skill development. These approaches leverage social dynamics to enhance educational outcomes.", "ai"),
    ("In this context, the assessment of student learning must encompass multiple modalities beyond traditional standardized testing. Comprehensive evaluation frameworks provide more holistic insights into academic progress and development.", "ai"),
    ("As a result of extensive research, project-based learning approaches have emerged as highly effective pedagogical methodologies. These comprehensive strategies facilitate deeper conceptual understanding and practical skill application.", "ai"),
    ("The strategic implementation of corporate social responsibility initiatives yields significant reputational benefits while simultaneously addressing broader societal concerns. Furthermore, these comprehensive programs enhance stakeholder relationships.", "ai"),
    ("It is worth noting that market volatility presents both challenges and opportunities for sophisticated investors. Leveraging quantitative analytical frameworks enables more robust portfolio management under conditions of uncertainty.", "ai"),
    ("In conclusion, organizational culture plays a pivotal role in determining long-term business performance. Comprehensive cultural transformation initiatives are absolutely essential for sustained competitive advantage in dynamic markets.", "ai"),
    ("The utilization of advanced customer relationship management systems provides substantial insights into consumer behavior patterns. Additionally, these robust platforms facilitate more personalized engagement strategies across multiple touchpoints.", "ai"),
    ("Furthermore, the implementation of agile methodologies has fundamentally transformed software development practices. These comprehensive frameworks enable organizations to respond more effectively to rapidly evolving market requirements.", "ai"),
    ("It should be noted that human capital represents perhaps the most valuable asset in knowledge-intensive industries. Robust talent acquisition and retention strategies are therefore absolutely essential for organizational success.", "ai"),
    ("The comprehensive analysis of competitive dynamics reveals that first-mover advantages, while significant, are not necessarily determinative of long-term market success. Leveraging sustainable competitive advantages requires continuous innovation.", "ai"),
    ("As demonstrated by empirical evidence, diversity and inclusion initiatives yield measurable performance improvements across multiple organizational dimensions. These comprehensive programs must therefore be thoughtfully designed and rigorously implemented.", "ai"),
    ("In this context, the optimization of operational processes through lean management principles provides substantial efficiency gains. Furthermore, these methodologies facilitate continuous improvement cultures within organizational structures.", "ai"),
    ("The intersection of behavioral economics and marketing strategy offers sophisticated insights into consumer decision-making processes. Leveraging these frameworks enables more effective and ethically responsible persuasive communication.", "ai"),
    ("The comprehensive assessment of carbon sequestration methodologies reveals significant variability in effectiveness across different geographical contexts. Furthermore, scalable implementation requires robust policy frameworks.", "ai"),
    ("It is important to note that biodiversity loss represents an existential threat to ecosystem stability. Comprehensive conservation strategies must leverage innovative approaches to address this multifaceted environmental challenge.", "ai"),
    ("In conclusion, the transition to circular economy principles requires fundamental transformation of production and consumption systems. Leveraging innovative materials science and industrial ecology concepts is absolutely essential.", "ai"),
    ("Additionally, urban planning frameworks that prioritize sustainable transportation and mixed-use development patterns yield substantial environmental co-benefits. These comprehensive approaches facilitate more livable and resilient communities.", "ai"),
    ("The evidence clearly demonstrates that corporate environmental commitments, when substantively implemented, yield both ecological benefits and long-term business value. Robust environmental management systems are therefore crucial.", "ai"),
    ("Furthermore, the development of nature-based solutions for climate adaptation represents a promising complement to engineered infrastructure approaches. These comprehensive strategies leverage ecosystem services to address vulnerability.", "ai"),
    ("It should be noted that water resource management faces unprecedented challenges due to climate variability and growing demand. Comprehensive integrated approaches are absolutely essential for ensuring long-term water security.", "ai"),
    ("The paradigm shift toward regenerative agricultural practices offers significant potential for simultaneously addressing food security and environmental sustainability. These holistic approaches fundamentally reconceptualize land stewardship.", "ai"),
    ("In this context, the role of indigenous knowledge in environmental management deserves substantially greater recognition. Comprehensive conservation frameworks should leverage traditional ecological knowledge alongside scientific approaches.", "ai"),
    ("As evidenced by mounting scientific consensus, immediate and ambitious greenhouse gas emissions reductions are absolutely essential. Leveraging all available mitigation pathways is crucial for limiting catastrophic climate impacts.", "ai"),
    ("The examination of democratic governance structures reveals significant variation in institutional effectiveness across different national contexts. Furthermore, robust civic engagement is absolutely essential for democratic vitality.", "ai"),
    ("It is worth noting that social capital represents a crucial determinant of community resilience and collective action capacity. Comprehensive community development strategies must therefore prioritize the cultivation of trust and reciprocity.", "ai"),
    ("In conclusion, immigration policy reform requires careful balancing of humanitarian obligations, economic considerations, and security imperatives. Comprehensive, evidence-based approaches are absolutely essential for effective policy development.", "ai"),
    ("The utilization of evidence-based approaches in criminal justice reform demonstrates significant potential for simultaneously reducing recidivism and promoting rehabilitation. Additionally, these frameworks address systemic inequities.", "ai"),
    ("Furthermore, the erosion of institutional trust represents a significant challenge to democratic governance. Robust transparency and accountability mechanisms are therefore absolutely essential for restoring public confidence.", "ai"),
    ("It should be noted that income inequality has reached historically significant levels in many advanced economies. Comprehensive policy interventions must address both the symptoms and structural drivers of this multifaceted challenge.", "ai"),
    ("The comprehensive analysis of media ecosystem transformations reveals profound implications for public discourse and democratic deliberation. Leveraging regulatory frameworks to address misinformation while preserving expression is crucial.", "ai"),
    ("As a result of extensive research, community-based participatory approaches demonstrate superior outcomes in addressing complex social challenges. These comprehensive methodologies leverage local knowledge and build sustainable capacity.", "ai"),
    ("In this context, the intersectionality of various forms of structural disadvantage requires sophisticated analytical frameworks. Comprehensive equity initiatives must address the complex interplay of race, class, gender, and other factors.", "ai"),
    ("The paradigmatic transformation of work due to technological automation necessitates proactive policy responses. Comprehensive workforce development strategies leveraging human-centered design principles are therefore absolutely essential.", "ai"),
    ("The comprehensive examination of postmodern aesthetic traditions reveals significant tensions between accessibility and conceptual complexity. Furthermore, these cultural dynamics reflect broader societal transformations.", "ai"),
    ("It is worth noting that cultural heritage preservation represents both a scholarly imperative and a community development opportunity. Robust documentation methodologies leverage digital technologies to safeguard endangered traditions.", "ai"),
    ("In conclusion, the globalization of cultural production has yielded both unprecedented cross-cultural exchange and concerning homogenization tendencies. These complex dynamics require nuanced analytical frameworks.", "ai"),
    ("The utilization of digital platforms for artistic expression has fundamentally democratized cultural participation. Additionally, these comprehensive tools enable new forms of collaborative creativity across geographical boundaries.", "ai"),
    ("Furthermore, the curation of contemporary art exhibitions requires sophisticated engagement with diverse cultural perspectives. Comprehensive inclusive practices are absolutely essential for meaningful representation and accessibility.", "ai"),
    ("It should be noted that narrative traditions across cultures serve crucial functions in transmitting values and constructing collective identity. These rich literary heritages deserve comprehensive scholarly attention and preservation.", "ai"),
    ("The intersection of technology and musical performance has yielded remarkable innovations in both composition and audience engagement. Leveraging these developments while preserving artistic authenticity represents a significant challenge.", "ai"),
    ("As demonstrated by anthropological research, ritual and ceremonial practices fulfill essential psychological and social functions across diverse cultural contexts. Comprehensive ethnographic approaches provide valuable insights.", "ai"),
    ("In this context, the preservation of linguistic diversity represents both a cultural imperative and a scientific opportunity. Comprehensive language revitalization programs leverage community engagement to sustain endangered languages.", "ai"),
    ("The paradigm of participatory culture facilitated by digital technologies has substantially transformed relationships between cultural producers and consumers. These comprehensive shifts necessitate reconceptualization of authorship and creativity.", "ai"),
    ("It is important to acknowledge that personal development requires sustained commitment and strategic intentionality. Leveraging evidence-based self-improvement methodologies facilitates more comprehensive and lasting transformation.", "ai"),
    ("In conclusion, effective time management necessitates the implementation of robust prioritization frameworks. Additionally, leveraging technology-enhanced productivity tools can substantially optimize personal and professional performance.", "ai"),
    ("The comprehensive assessment of relationship dynamics reveals that effective communication skills represent perhaps the most crucial determinant of interpersonal success. Furthermore, empathy plays a pivotal role in fostering connection.", "ai"),
    ("Furthermore, the cultivation of emotional intelligence yields substantial benefits across both personal and professional domains. It is worth noting that these competencies can be systematically developed through deliberate practice.", "ai"),
    ("As a result of extensive psychological research, growth mindset orientations are strongly associated with greater resilience and achievement. Leveraging this framework enables more adaptive responses to challenges and setbacks.", "ai"),
    ("It should be noted that financial literacy represents a crucial life skill with profound implications for long-term wellbeing. Comprehensive financial education programs are absolutely essential for empowering informed decision-making.", "ai"),
    ("The utilization of mindfulness practices in daily routines yields significant benefits for psychological wellbeing and cognitive performance. These evidence-based approaches are certainly worth incorporating into comprehensive wellness strategies.", "ai"),
    ("In this context, the development of leadership capabilities requires systematic cultivation of both technical competencies and interpersonal skills. Comprehensive leadership development programs must address this multifaceted nature.", "ai"),
    ("The synthesis of positive psychology research suggests that meaningful social connections represent a primary determinant of subjective wellbeing. Leveraging community-based approaches can facilitate greater belonging and flourishing.", "ai"),
    ("Of course, achieving work-life balance requires intentional boundaries and strategic prioritization. Robust self-care practices are absolutely essential for maintaining sustainable performance across personal and professional dimensions.", "ai"),
    ("The comprehensive evaluation of nutritional supplementation research reveals significant heterogeneity in study quality and findings. Furthermore, individual variability necessitates personalized approaches to dietary optimization.", "ai"),
    ("It is worth emphasizing that travel represents a profoundly enriching opportunity for cultural exchange and personal development. Leveraging immersive experiences facilitates deeper cross-cultural understanding and broadens perspectives.", "ai"),
    ("In conclusion, pet ownership yields substantial psychological benefits including reduced stress and enhanced social connection. These comprehensive wellness effects make companion animals valuable contributors to human flourishing.", "ai"),
    ("Additionally, home organization methodologies based on intentional curation and systematic storage solutions yield significant benefits for both cognitive clarity and aesthetic satisfaction. Robust frameworks facilitate sustainable tidiness.", "ai"),
    ("The paradigm of sustainable consumption requires fundamental reconceptualization of our relationship with material possessions. Comprehensive minimalist approaches leverage intentionality to align purchasing decisions with core values.", "ai"),
    ("Furthermore, the evidence strongly supports the conclusion that regular engagement with nature yields significant restorative psychological benefits. Leveraging green spaces in urban environments is therefore absolutely essential.", "ai"),
    ("It should be noted that culinary traditions represent a rich intersection of cultural heritage, scientific knowledge, and creative expression. Comprehensive gastronomic education encompasses both technical skill development and cultural appreciation.", "ai"),
    ("The intersection of technology and interpersonal communication has fundamentally transformed social dynamics. It is important to recognize that these comprehensive changes necessitate new frameworks for navigating digital relationships.", "ai"),
    ("As evidenced by research, adequate sleep represents perhaps the most foundational pillar of physical and mental health. Robust sleep hygiene practices are therefore absolutely essential for sustained cognitive performance.", "ai"),
    ("In this context, the curation of personal learning journeys requires strategic alignment of educational resources with individual goals. Leveraging diverse knowledge acquisition modalities facilitates more comprehensive skill development.", "ai"),
    ("I was so tired yesterday I literally fell asleep on my keyboard lol. Woke up with 'gggggggg' in my email draft to my boss. Not my finest moment honestly.", "human"),
    ("ok so I tried making that pasta recipe you sent me and it was... not great? I think I added too much salt but also the sauce was kinda watery. idk what went wrong", "human"),
    ("Can't believe it's already Friday! This week absolutely flew by. Met up with Jake for coffee and we ended up talking for like 3 hours about everything and nothing.", "human"),
    ("Just got back from the dentist. Two cavities. TWO. I brush my teeth every day, this is honestly so unfair. Also the waiting room had the most depressing music playing.", "human"),
    ("my dog did the funniest thing this morning - she brought me my shoe and just sat there staring at me like 'are we going or what?' she's honestly smarter than me", "human"),
    ("I've been thinking a lot about whether to switch jobs lately. Part of me is excited about the new opportunity but I'm also really comfortable where I am and change is scary you know?", "human"),
    ("FINALLY finished that book I've been reading for like 6 months. The ending was not what I expected at all - kinda disappointed but also? Kind of impressed by the twist.", "human"),
    ("Had the worst commute today. Train was delayed 40 minutes, then some guy spilled his coffee on my jacket. Just one of those days I guess. At least the coffee smelled nice.", "human"),
    ("ngl I've been pretty stressed about money lately. like I know I need to budget better but somehow there's always something that comes up. car repairs this month, dentist next", "human"),
    ("My mom called three times while I was in a meeting. Called back and she just wanted to tell me about a bird that landed on her porch. I love her so much.", "human"),
    ("Started learning guitar two weeks ago and I'm... not good. My fingers hurt constantly and my cat leaves the room every time I practice. Baby steps I guess!", "human"),
    ("Went hiking with friends this weekend and completely underestimated the trail difficulty. We were supposed to do 5 miles but ended up doing 12 somehow??? Still not sure how that happened.", "human"),
    ("The coffee shop I always go to changed their WiFi password and won't tell customers anymore. Kind of brutal honestly. Been going there every day for two years.", "human"),
    ("I know everyone says meal prep is life-changing but I genuinely cannot make myself do it on Sundays. I always have big plans and then end up watching TV instead.", "human"),
    ("Just realized I've been mispronouncing 'quinoa' for years. Like years. Had a whole conversation at a dinner party last week. Nobody corrected me. I'm choosing to be grateful.", "human"),
    ("my apartment is cold but I also don't want to pay more for heat so I'm just wearing like 3 sweaters indoors and pretending I'm camping. this is fine. I'm fine.", "human"),
    ("Finally saw that movie everyone was talking about and I have thoughts! First of all the pacing in the second act was rough. But that ending scene? Genuinely moved me. 8/10.", "human"),
    ("Had a job interview today and I think it went okay? Hard to tell. I always leave those things convinced I either absolutely nailed it or completely bombed it, never in between.", "human"),
    ("Bought a plant. It's called a pothos and the internet says it's impossible to kill. I've already killed it once, I think. Looking a little sad. Please send thoughts and prayers.", "human"),
    ("My neighbor started playing drums at 11pm last night. I knocked, we had a very polite conversation, and then he kept playing until 1am. Truly unbelievable.", "human"),
    ("Made pancakes this morning and they were actually really good?? I've been trying for years and I think the secret is just... not flipping them too early. Revolutionary information.", "human"),
    ("I was supposed to go to the gym today. Instead I watched a 2-hour documentary about competitive cheese rolling. No regrets. Well. Some regrets. But mostly none.", "human"),
    ("spent 3 hours debugging this error today and it turned out to be a missing semicolon. THREE HOURS. I need to find a new career honestly", "human"),
    ("just discovered you can use ctrl+shift+t to reopen closed tabs and my whole life has changed. how did nobody tell me this for 10 years", "human"),
    ("our company switched to a new project management tool and now i can't find anything. spent 20 minutes looking for the thing i do every day. innovation!!", "human"),
    ("my wifi keeps dropping every time someone in my house uses the microwave. 2024 and this is still a thing that happens. incredible.", "human"),
    ("worked from home today and realized I haven't left my apartment in 4 days. sent myself on a 'meeting walk' to the corner store. productivity guru stuff.", "human"),
    ("I've been in so many meetings this week that could have been emails. genuinely think my brain is 40% conference call audio at this point", "human"),
    ("laptop fan started making a noise that sounds exactly like a small helicopter taking off. my coworkers on zoom can definitely hear it. very professional.", "human"),
    ("tried to 'automate' my morning routine and now I have 47 browser tabs open across 3 windows every day. I've created a monster.", "human"),
    ("my phone autocorrected 'I'll be there soon' to 'I'll be cheese soon' and I sent it before I noticed. my boss just replied 'ok cheese'", "human"),
    ("finally cleaned up my downloads folder - 3 years of random PDFs, screenshots, and approximately 200 copies of the same stock photo. very normal stuff", "human"),
    ("made soup from scratch today for the first time and it took four hours and tasted exactly like the $2 can of soup from the store. totally worth it", "human"),
    ("ordered pizza and they put the toppings in alphabetical order on the pizza. artichoke, basil, chicken. nobody asked for this but honestly respect.", "human"),
    ("tried a recipe that said 'quick and easy - 15 minutes!' and it took me an hour and twenty minutes. i have so many questions about who they tested this on", "human"),
    ("accidentally bought full-fat coconut milk instead of the light kind. made the curry anyway. it was incredible. maybe this is just who I am now", "human"),
    ("my sourdough starter has officially outlived two houseplants and a relationship. it's the most stable thing in my life and that's fine.", "human"),
    ("made cookies and forgot to add sugar. somehow didn't realize until they were done. they taste like buttery sadness but I'm eating them anyway.", "human"),
    ("at what age do you start genuinely enjoying vegetables without forcing yourself? asking for me, a 34-year-old who still doesn't love broccoli", "human"),
    ("roommate made their 'world famous chili' and it was... just beans. like plain beans with some powder on them. I have to find a new place to live.", "human"),
    ("convinced myself the leftover pasta was still good. it was not. I knew it wasn't. I ate it anyway. this is who I am as a person.", "human"),
    ("the grocery store moved everything around and I've been accidentally buying the wrong yogurt for three weeks. loyalty means nothing anymore.", "human"),
    ("texted someone happy birthday and they replied 'lol thanks'. I wrote a whole paragraph. anyway everything is fine and I'm not thinking about it", "human"),
    ("ran into my ex at the coffee shop and we both pretended not to see each other for 20 minutes while standing 6 feet apart. very normal adult behavior", "human"),
    ("got a passive aggressive email from a coworker and spent 45 minutes crafting the perfect reply and then sent 'sounds good, thanks!' I think I won???", "human"),
    ("friend group is trying to plan a dinner and we've been in a group chat for 3 weeks and haven't picked a date. democracy doesn't work.", "human"),
    ("told my friend I'd be there in 5 minutes, left 20 minutes later, somehow still arrived early. time works differently in my universe.", "human"),
    ("my coworker microwaves fish every single friday and I have just accepted this is my life now. some battles aren't worth fighting.", "human"),
    ("said 'you too' when a cashier told me to enjoy my meal. then said it again when they repeated it, clearly just being polite. had to leave the country briefly.", "human"),
    ("accidentally liked a photo from 3 years ago on someone's instagram and I've been thinking about it every 20 minutes for the past two days", "human"),
    ("asked my roommate to please do their dishes and they started doing ALL the dishes including mine as a power move and now I don't know what to do", "human"),
    ("friend cancelled on me twice this month and now when they text I wait exactly as long as they took to respond to me. I'm a grown adult doing this.", "human"),
    ("started running last month. my lungs hate me, my knees hate me, my neighbors who see me gasping at 7am definitely judge me. but I'm doing it!", "human"),
    ("doctor told me to 'reduce stress' as if I could just do that. I'll add it to my stress list. number 7 on the list: stop being stressed.", "human"),
    ("went to the gym for the first time in 4 months and now I cannot lift my arms above my head. totally proportional response from my body.", "human"),
    ("convinced myself I could handle a 'beginner' yoga class. there were multiple moments where I wasn't sure I was going to survive. the instructor was lovely about it.", "human"),
    ("my fitbit informed me I haven't hit my step goal in 11 days. I have chosen to interpret this as the fitbit being wrong.", "human"),
    ("decided to try intermittent fasting. made it until 11am. ate an entire sleeve of crackers. honestly impressive I lasted that long.", "human"),
    ("bought a standing desk. stand at it for approximately 12 minutes per day. sit the rest of the time and feel vaguely guilty. $400 well spent.", "human"),
    ("my body thinks 3am is a great time to be fully awake and ready to think about every decision I made since 2008. very helpful, thanks brain.", "human"),
    ("tried meditation for the first time and spent the whole time thinking about whether I was doing it right. so that's going well.", "human"),
    ("the doctor said 'you should be exercising more' and then looked at my chart and said it again but slower. rude but fair.", "human"),
    ("got to the airport 3 hours early because I'm anxious and then my gate was literally the last one in the terminal. I walked so far. worth it for the calm.", "human"),
    ("went to a new restaurant and the menu had no prices on it. I ordered anyway and now I'm scared to see the bill. adventure is part of the experience I guess.", "human"),
    ("visited my hometown after 5 years and everything is completely different except my high school which looks exactly the same. time is weird.", "human"),
    ("took a wrong turn on a hike and accidentally found the most beautiful view I've ever seen. sometimes getting lost is the whole point I think.", "human"),
    ("road trip with friends means arguing about the playlist for 6 hours straight. we've compromised on a playlist that nobody actually likes. democracy!", "human"),
    ("the hotel said it had a 'city view' which turned out to be a view of the parking garage. still a city technically. I respect the creativity.", "human"),
    ("traveling alone for the first time and I keep starting to say something and then remembering I'm alone and it's just me and the gelato and that's fine.", "human"),
    ("sat next to a really interesting person on the plane, had a great conversation for 4 hours, both stood up at landing and went our separate ways forever. wild.", "human"),
    ("ordered something from the menu I couldn't quite read in Italian and got a whole fish with the head still on. excellent surprise. ate it with confidence.", "human"),
    ("visited 4 museums in one day and then spent the evening unable to absorb any more information, staring at a wall. this is called culture apparently.", "human"),
    ("I've been really tired lately. not sleeping badly but just... tired in a different way. not sure what to do about it. probably need to go outside more.", "human"),
    ("cleaned my whole apartment on a whim at midnight and now it's 2am and I'm very awake and also proud. this is normal adult behavior.", "human"),
    ("called my dad just to say hi and we talked for an hour about nothing. he's really funny. I don't know why I don't do that more often.", "human"),
    ("watched an old video of my dog when she was a puppy and immediately started crying. she's right next to me currently. perfectly fine. just feeling things.", "human"),
    ("sometimes I wonder if I'm doing the right thing with my life and then I eat some cheese and feel better about everything. cheese is very stabilizing.", "human"),
    ("sent a thank you note to someone who helped me last year and they responded saying they really needed that today. small things matter I think.", "human"),
    ("drove past my old apartment and had this huge wave of nostalgia for a time that was honestly kind of rough. memory is doing something interesting there.", "human"),
    ("finished a project I've been working on for months and felt happy for like 10 minutes and then immediately started worrying about the next one. very me.", "human"),
    ("I'm 32 and I still don't know how to talk to my parents about hard stuff. hoping we'll all figure it out eventually. seems fine.", "human"),
    ("really embarrassed myself in a meeting today and spent 3 hours replaying it. sent a short apology email. they responded 'haha no worries'. already forgotten by everyone except me.", "human"),
    ("finally watched that show everyone was obsessed with two years ago. I get it. I completely get it. I should have listened. currently devastated it's over.", "human"),
    ("tried the 'life-changing' organization system from that book everyone read and honestly it's just putting things in boxes but labeled. effective though?", "human"),
    ("the new update changed where the settings button is. I've pressed the wrong thing 15 times today. they moved it ONE pixel to the left. why.", "human"),
    ("this coffee shop makes coffee that is too good. I shouldn't be allowed to have this every day. dangerous establishment. already planning my return tomorrow.", "human"),
    ("bought the expensive headphones everyone recommended and they're incredible and now I'm sad because I wasted years with bad audio. can't go back.", "human"),
    ("the book everyone said changed their life was fine. good, even. not life-changing. my life remains unchanged but I did enjoy parts of it.", "human"),
    ("took a 'quick' scroll through social media and lost an hour. genuinely no memory of what I saw. just gone. time just evaporated.", "human"),
    ("got really into a podcast about something I previously had zero interest in and now I know way too much about competitive bridge. this is my life.", "human"),
    ("the recommended algorithm figured out what I want before I did. watching a documentary about something I didn't know existed and I'm completely hooked.", "human"),
    ("saw a movie without reading any reviews first for the first time in years and the experience of having no expectations was incredible. recommend to everyone.", "human"),
    ("I don't really know how to explain this but I've been feeling kind of off lately? not sad exactly just like slightly out of step with everything. probably just a phase.", "human"),
    ("my sister and I had the same exact childhood and are completely different people. she's organized, decisive, has a 5-year plan. I have a snack in my pocket.", "human"),
    ("found $20 in an old jacket and felt genuinely wealthy for approximately one afternoon. bought a fancy coffee and some fruit. very responsible.", "human"),
    ("the self-checkout machine kept asking me to place my item in the bagging area and I had already placed it there and we were at an impasse for 2 full minutes.", "human"),
    ("asked someone how they were doing and they told me and it was really interesting and I realized I should ask this question and actually listen more often.", "human"),
    ("locked myself out of my apartment for the second time this year. called the locksmith. he recognized me. we have a relationship now.", "human"),
    ("it rained today and my whole mood shifted. I don't know why weather has so much power over me. I just love rain I think. very calming.", "human"),
    ("bought something expensive and feel bad and also good simultaneously. this is the full range of the shopping experience I guess. complicated emotions.", "human"),
    ("tried to explain something I care about to someone who doesn't care about it and they were very polite and I could tell they weren't listening. that's okay.", "human"),
    ("spent an evening doing absolutely nothing productive and I feel great about it. sometimes the nothing is exactly what you needed. very restorative.", "human"),
    ("update: my laptop has been slow for a month and the 'solution' was to restart it. I am a technology professional. I did not try this for a month.", "human"),
    ("bought a smart bulb so I could control my lights with my phone. it takes 4 steps and my old switch was 1 step. progress is complicated.", "human"),
    ("my spreadsheet works perfectly and I'm scared to touch it. it's a delicate ecosystem at this point. I'm afraid of it honestly.", "human"),
    ("set up automatic bill payments and then forgot I did it and panicked at a charge for three minutes before remembering. future me is helpful but sneaky.", "human"),
    ("subscribed to a free trial, forgot, was charged, cancelled, immediately missed the service, resubscribed. this cycle has happened 3 times.", "human"),
    ("deleted an email thinking it was spam and it wasn't. spent 45 minutes in the deleted folder. found it. sent the response. everything is fine. I'm fine.", "human"),
    ("wrote something really good in my notes app and then couldn't find it for 4 days. still not sure how. it was right there. notes apps are portals.", "human"),
    ("the website asked if I accept cookies and I said yes without thinking and then thought about it for a second too long after and now feel weird about it", "human"),
    ("tried to set a reminder and accidentally set it for 3am. woke up very confused. my phone is smarter than me and also more annoying.", "human"),
    ("password reset emails are sent instantly. everything else takes a day. the internet is very clear about its priorities and so am I.", "human"),
]


def compute_heuristic_score(text):
    score = 0.5
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    words = text.split()
    lower = text.lower()

    if not sentences or not words:
        return score

    lengths = [len(s.split()) for s in sentences]
    avg_len = sum(lengths) / len(lengths)
    variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)

    if avg_len > 22:     score += 0.07
    if avg_len > 28:     score += 0.05
    if variance < 10:    score += 0.08
    if variance > 60:    score -= 0.06

    ai_phrases = [
        'furthermore', 'additionally', 'in conclusion', 'it is worth noting',
        'it is important to', 'in this context', 'as mentioned', 'delve',
        'utilize', 'comprehensive', 'robust', 'leverage', 'paradigm',
        'it should be noted', 'plays a crucial role', 'as a result',
        'with that said', 'absolutely essential', 'of course', 'certainly',
        'necessitates', 'multifaceted', 'holistic', 'intricate interplay',
        'yield substantial', 'facilitate', 'subsequently', 'underscore',
        'moreover', 'notwithstanding', 'in summary', 'as evidenced by',
        'empirical evidence', 'unequivocally', 'paramount', 'foundational',
        'transformative', 'unprecedented', 'innovative solutions',
        'moving forward', 'at its core', 'going forward', 'it is crucial',
        'plays a pivotal', 'a testament to',
    ]
    matches = sum(1 for p in ai_phrases if p in lower)
    score += min(matches * 0.035, 0.22)

    human_signals = [
        'lol', 'ngl', 'tbh', 'idk', 'omg', 'wtf', 'lmao', 'bruh',
        'literally', 'honestly', 'kinda', 'gonna', 'wanna', 'gotta',
        'stuff', 'thing', 'anyway', 'somehow', 'apparently',
        'pretty much', 'sort of', 'kind of', 'a lot', 'way too',
    ]
    human_matches = sum(1 for h in human_signals if h in lower)
    score -= min(human_matches * 0.05, 0.20)

    contractions = len(re.findall(
        r"\b\w+n't\b|\b(I'm|you're|they're|we're|it's|don't|can't|won't|I've|I'd|wouldn't|couldn't|shouldn't|isn't|aren't|weren't)\b",
        text, re.I))
    if contractions == 0 and len(words) > 50:
        score += 0.07
    elif contractions >= 3:
        score -= 0.09

    score -= min(text.count('!') * 0.04, 0.12)
    score -= min(text.count('?') * 0.02, 0.06)

    caps_words = len(re.findall(r'\b[A-Z]{2,}\b', text))
    if caps_words > 0:
        score -= min(caps_words * 0.03, 0.09)

    if '...' in text or '\u2026' in text:
        score -= 0.06
    if ' - ' in text or '\u2014' in text:
        score -= 0.03

    casual = len(re.findall(r'\b(I|me|my|mine|myself)\b', text))
    if casual > 4:
        score -= 0.07
    elif casual > 1:
        score -= 0.03

    if re.search(r'\byou know\b|\bright\?\b|\bI mean\b|\bI guess\b|\bI think\b', lower):
        score -= 0.05

    digit_count = len(re.findall(r'\b\d+\b', text))
    if digit_count > 3 and avg_len < 20:
        score -= 0.04

    passive = len(re.findall(r'\b(is|are|was|were|be|been|being)\s+\w+ed\b', lower))
    score += min(passive * 0.03, 0.10)

    return max(0.02, min(0.98, score))


class SklearnDetector:
    def __init__(self):
        self.pipeline = None
        self.trained = False

    def train(self, samples):
        texts  = [t for t, _ in samples]
        labels = [1 if l == 'ai' else 0 for _, l in samples]
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 3), min_df=1, max_features=15000,
                sublinear_tf=True, analyzer='word', strip_accents='unicode',
            )),
            ('clf', LogisticRegression(C=1.5, max_iter=1000, class_weight='balanced', solver='lbfgs')),
        ])
        self.pipeline.fit(texts, labels)
        self.trained = True

    def predict(self, text):
        ml  = float(self.pipeline.predict_proba([text])[0][1])
        heu = compute_heuristic_score(text)
        final = 0.75 * ml + 0.25 * heu
        label = 'ai' if final > 0.5 else 'human'
        conf  = final if label == 'ai' else (1 - final)
        return {
            'label':      label,
            'confidence': round(conf * 100, 1),
            'score':      round(final, 4),
            'ml_score':   round(ml, 4),
            'heuristic':  round(heu, 4),
        }


class NaiveBayesDetector:
    def __init__(self):
        self.ai_word_freq    = Counter()
        self.human_word_freq = Counter()
        self.ai_total = 0
        self.human_total = 0
        self.vocab = set()

    def tokenize(self, text):
        return re.findall(r'\b[a-z]{2,}\b', text.lower())

    def train(self, samples):
        for text, label in samples:
            tokens = self.tokenize(text)
            if label == 'ai':
                self.ai_word_freq.update(tokens)
                self.ai_total += len(tokens)
            else:
                self.human_word_freq.update(tokens)
                self.human_total += len(tokens)
        self.vocab = set(self.ai_word_freq) | set(self.human_word_freq)

    def log_prob(self, tokens, freq, total):
        V = len(self.vocab)
        return sum(math.log((freq.get(t, 0) + 1) / (total + V)) for t in tokens)

    def predict(self, text):
        tokens = self.tokenize(text)
        if not tokens:
            return {'label': 'unknown', 'confidence': 0, 'score': 0.5, 'ml_score': 0.5, 'heuristic': 0.5}
        log_ai    = math.log(0.5) + self.log_prob(tokens, self.ai_word_freq, self.ai_total)
        log_human = math.log(0.5) + self.log_prob(tokens, self.human_word_freq, self.human_total)
        max_log   = max(log_ai, log_human)
        ai_prob   = math.exp(log_ai - max_log)
        hum_prob  = math.exp(log_human - max_log)
        ai_score  = ai_prob / (ai_prob + hum_prob)
        heu       = compute_heuristic_score(text)
        final     = 0.65 * ai_score + 0.35 * heu
        label = 'ai' if final > 0.5 else 'human'
        conf  = final if label == 'ai' else (1 - final)
        return {
            'label':      label,
            'confidence': round(conf * 100, 1),
            'score':      round(final, 4),
            'ml_score':   round(ai_score, 4),
            'heuristic':  round(heu, 4),
        }


MODEL_PATH = 'model.pkl'

def load_or_train():
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, 'rb') as f:
                return pickle.load(f)
        except Exception:
            pass
    det = SklearnDetector() if SKLEARN_AVAILABLE else NaiveBayesDetector()
    det.train(DATASET)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(det, f)
    return det

detector = load_or_train()

def get_cv_accuracy():
    if not SKLEARN_AVAILABLE:
        return None
    try:
        texts  = [t for t, _ in DATASET]
        labels = [1 if l == 'ai' else 0 for _, l in DATASET]
        pipe = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 3), min_df=1, max_features=15000, sublinear_tf=True)),
            ('clf',   LogisticRegression(C=1.5, max_iter=1000, class_weight='balanced')),
        ])
        scores = cross_val_score(pipe, texts, labels, cv=5, scoring='accuracy')
        return round(float(np.mean(scores)) * 100, 1)
    except Exception:
        return None

CV_ACCURACY = get_cv_accuracy()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/detect', methods=['POST'])
def detect():
    data = request.get_json(silent=True) or {}
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    if len(text) < 20:
        return jsonify({'error': 'Text too short (min 20 characters)'}), 400
    result = detector.predict(text)
    result['word_count']  = len(text.split())
    result['char_count']  = len(text)
    result['model_type']  = 'TF-IDF + Logistic Regression' if SKLEARN_AVAILABLE else 'Naive Bayes'
    return jsonify(result)


@app.route('/api/dataset/stats')
def dataset_stats():
    ai_count    = sum(1 for _, l in DATASET if l == 'ai')
    human_count = sum(1 for _, l in DATASET if l == 'human')
    try:
        vocab_size = len(detector.pipeline.named_steps['tfidf'].vocabulary_)
    except Exception:
        vocab_size = len(getattr(detector, 'vocab', set()))
    return jsonify({
        'total':       len(DATASET),
        'ai':          ai_count,
        'human':       human_count,
        'vocab':       vocab_size,
        'model':       'TF-IDF + Logistic Regression' if SKLEARN_AVAILABLE else 'Naive Bayes',
        'cv_accuracy': CV_ACCURACY,
        'ngrams':      '1-3' if SKLEARN_AVAILABLE else 'unigrams',
        'features':    '15000' if SKLEARN_AVAILABLE else str(vocab_size),
    })


if __name__ == '__main__':
    print(f"AI Text Detector running on http://localhost:5000")
    print(f"Model: {'TF-IDF + Logistic Regression' if SKLEARN_AVAILABLE else 'Naive Bayes'}")
    print(f"Dataset: {len(DATASET)} samples")
    if CV_ACCURACY:
        print(f"5-fold CV Accuracy: {CV_ACCURACY}%")
    app.run(debug=True, port=5000)
