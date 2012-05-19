"""
Richard Littauer
Code for cleaning Rangi Facebook group.
March 30, 2012

Released under no copywright, probably because this won't be released at all.

"""

import sys
import time
import re
import urllib, urllib2
from BeautifulSoup import BeautifulSoup

file = 'file:///Users/richardlittauer/Documents/Research/Topics/Rangi/' + sys.argv[1]
output_file_name = 'output_raw'
output = open(output_file_name,'w+')
u = urllib2.urlopen(file)

# mung it all together
rawhtml = "".join(map(str.strip,u.readlines()))
bs = BeautifulSoup(rawhtml)

output.write('<text id="Rangi_scrape" source_id="rangi_scrape" title="Rangi \
        Facebook clean">')
output.write('<metadata idref="Rangi_clean">\
         <!-- incorporate OLAC metadata standard -->\
         </metadata>')
output.write('<body>')

print 'Using file.'

authors = {}
author_id = 1
source_id = 1

story = bs.findAll('div', {'class': 'storyContent'})

for le in story:

    thread_id = story.index(le) + 1
    print 'Thread: ' + str(thread_id)
    output.write('<thread id="' + str(thread_id) + '">')

    comment_id = 1
    com_idref= str(thread_id) + '.' + str(comment_id)

    output.write('<comment id="' + com_idref +\
            '" idref="' + str(thread_id) + '">')

    if len(le.find('div', {'class': 'mainWrapper'}).findAll('h6')) == 2:

        # This should get only the first commenter, and the href
        if le.find('div', {'class': 'actorDescription actorName'}) != None:
            actor = le.find('div', {'class': 'actorDescription actorName'}).find('a') 
            actor_name = str(actor.contents[0])
            actor_href = str(actor['href'])
            if actor_name not in authors:
                authors[actor_name] = author_id, actor_href
                current_id = author_id
                author_id += 1
            if actor_name in authors: current_id = authors[actor_name][0]

            # Write the author tag
            output.write('<author id="'+str(current_id)+\
                    '" idref="'+com_idref+'" url="'\
                    +actor_href+'">')
            output.write(actor_name + '</author>')
        if le.find('div', {'class':\
                'actorDescription uiStreamRobotextBeforeMessage'}) != None:
            actor = le.find('div', {'class':\
                'actorDescription uiStreamRobotextBeforeMessage'})\
                .find('a')
            actor_name = str(actor.contents[0])
            actor_href = str(actor['href'])
            if actor_name not in authors:
                authors[actor_name] = author_id, actor_href
                current_id = author_id
                author_id += 1
            if actor_name in authors: current_id = authors[actor_name][0]

            # Write the author tag
            output.write('<author id="'+str(current_id)+\
                    '" idref="'+com_idref+'" url="'\
                    +actor_href+'">')
            output.write(actor_name + '</author>')

        # This should get the time, in utime format
        time = le.find('span', {'class': 'uiStreamSource'})\
                .find('abbr')
        utime = time['data-utime']
        time_readable = time['title']

        # Write the timestamp tag
        output.write('<timestamp idref="'+com_idref+'" utime="'\
                +str(utime)+'">')
        output.write(time_readable)
        output.write('</timestamp>')

        # Who likes this comment?
        if le.find('div', {'class': \
                'UIImageBlock_Content UIImageBlock_ICON_Content'}) != None:

            likes = le.find('div', {'class': \
                    'UIImageBlock_Content UIImageBlock_ICON_Content'}).find('a')
            like_name = str(likes.contents[0])
            if like_name[-6:] != 'people':
                like_href = likes['href']
                if like_name not in authors:
                    authors[like_name] = author_id, like_href
                    current_id = author_id
                    author_id += 1
                if like_name in authors: current_id = authors[actor_name][0]
                like_author = authors[like_name][0]
                if like_href != authors[like_name][1]: 
                    print 'Error in likes author'

                like_id = 1

                output.write('<likes id="'+com_idref+'.'+str(like_id)+'" \
                        idref="'+com_idref+'">')
                output.write('<like_author id="'+str(like_author)+'" \
                        idref="'+com_idref+'.'+str(like_id)+'" url="'+\
                        like_href+'">')
                output.write(like_name)
                output.write('</like_author>')
                output.write('</likes>')
            if like_name[-6:] == 'people':

                likes = like_name[:-7]
                if likes != 0:
                    output.write('<likes id="'+com_idref+'.'+str(like_id)+'" \
                            idref="'+com_idref+'">')
                    output.write('<likes_total idref="'+\
                            com_idref+'.'+str(like_id)+'">')
                    output.write(likes)
                    output.write('</likes_total>')
                    output.write('</likes>')


        # Done on a mobile?
        mobile = le.find('a', {'href': '/mobile/?v=web'})
        if mobile != None:
            mobile = mobile.contents[0]

            output.write('<source id="'+str(source_id)+\
                    '" idref="'+com_idref+'">')
            output.write(mobile)
            output.write('</source>')

            source_id += 1


        # This should get the first message
        if len(le.find('span', {'class': 'messageBody'})) != 0:
            message = le.find('span', {'class': 'messageBody'}).contents
            # This removes all tags. It does handle the data,
            # But makes text much easier to get.
            for x in range(len(message)):
                message[x] = re.sub(r'<.*>', '', str(message[x]))
            message = ' '.join(message)
        if len(le.find('span', {'class': 'messageBody'})) == 0:
            message = ''

        output.write('<plaintext idref="'+com_idref+'">')
        output.write(message)
        output.write('</plaintext>')

        ## Phrase id, word id needs to be done. 

        output.write('</comment>')

    if len(le.find('div', {'class': 'mainWrapper'}).findAll('h6')) == 1:

        # This should get only the first commenter, and the href
        actor = le.find('h6', {'class': \
                'uiStreamMessage uiStreamHeadline uiStreamPassive'})\
                        .findAll('a')
        if len(actor) == 2:
            lead_actor = actor[0]
            second_actor = actor[1]
            actor_name = str(lead_actor.contents[0])
            actor_href = str(lead_actor['href'])
            if actor_name not in authors:
                authors[actor_name] = author_id, actor_href
                current_id = author_id
                author_id += 1
            if actor_name in authors: current_id = authors[actor_name][0]

            # Write the author tag
            output.write('<author id="'+str(current_id)+\
                    '" idref="'+com_idref+'" url="'\
                    +actor_href+'">')
            output.write(actor_name + '</author>')

            actor_name = str(second_actor.contents[0])
            actor_href = str(second_actor['href'])
            if actor_name not in authors:
                authors[actor_name] = author_id, actor_href
                current_id = author_id
                author_id += 1
            if actor_name in authors: current_id = authors[actor_name][0]

            # Write the author tag
            output.write('<author id="'+str(current_id)+\
                    '" idref="'+com_idref+'" url="'\
                    +actor_href+'">')
            output.write(actor_name + '</author>')

        # This should get the time, in utime format
        time = le.find('span', {'class': 'uiStreamSource'})\
                .find('abbr')
        utime = time['data-utime']
        time_readable = time['title']

        # Write the timestamp tag
        output.write('<timestamp idref="'+com_idref+'" utime="'\
                +str(utime)+'">')
        output.write(time_readable)
        output.write('</timestamp>')

        # Who likes this comment?
        try:
            likes = le.find('div', {'class': \
                    'UIImageBlock_Content UIImageBlock_ICON_Content'}).find('a')
            like_name = str(likes.contents[0])
            if like_name[-6:] != 'people':
                like_href = likes['href']
                if like_name not in authors:
                    authors[like_name] = author_id, like_href
                    current_id = author_id
                    author_id += 1
                if like_name in authors: current_id = authors[actor_name][0]
                like_author = authors[like_name][0]
                if like_href != authors[like_name][1]: 
                    print 'Error in likes author'

                like_id = 1

                output.write('<likes id="'+com_idref+'.'+str(like_id)+'" \
                        idref="'+com_idref+'">')
                output.write('<like_author id="'+str(like_author)+'" \
                        idref="'+com_idref+'.'+str(like_id)+'" url="'+\
                        like_href+'">')
                output.write(like_name)
                output.write('</like_author>')
                output.write('</likes>')

            if like_name[-6:] == 'people':

                likes = like_name[:-7]
                if likes != 0:
                    output.write('<likes id="'+com_idref+'.'+str(like_id)+'" \
                            idref="'+com_idref+'">')
                    output.write('<likes_total idref="'+\
                            com_idref+'.'+str(like_id)+'">')
                    output.write(likes)
                    output.write('</likes_total>')
                    output.write('</likes>')

        except: empty_variable = 'empty_variable'

        # Done on a mobile?
        mobile = le.find('a', {'href': '/mobile/?v=web'})
        if mobile != None:
            mobile = mobile.contents[0]

            output.write('<source id="'+str(source_id)+\
                    '" idref="'+com_idref+'">')
            output.write(mobile)
            output.write('</source>')

            source_id += 1

        # This should get the first message
        try:
            if int(len(le.find('span', {'class': 'caption'}).contents)) == 0:
                output.write('<plaintext idref="'+com_idref+'" />')
            if int(len(le.find('span', {'class': 'caption'}).contents)) > 0:

                message = le.find('span', {'class': 'caption'}).contents

                # This removes all tags. It does handle the data,
                # But makes text much easier to get.
                for x in range(len(message)):
                    message[x] = re.sub(r'<.*>', '', str(message[x]))
                message = ' '.join(message)

                output.write('<plaintext idref="'+com_idref+'">')
                output.write(message)
                output.write('</plaintext>')

        except: 
            if le.find('h6', {'data-ft': '{"type":1}'}).contents[1]\
                     == 'added':
                output.write('<plaintext idref="'+com_idref+'" />')

        ## Phrase id, word id needs to be done. 

        output.write('</comment>')

    # Find the comments
    cli = le.find('ul', {'class': 'commentList'})
    comments = cli.findAll('div', {'data-ft': '{"type":33}'})

    # Go through each one
    for comment in comments:

        comment_id += 1

        com_idref = str(thread_id) + '.' + str(comment_id)

        output.write('<comment id="' + com_idref +\
                '" idref="' + str(thread_id) + '">')

        # Find the commenter name and url
        commenter = comment.find('a', {'class': 'actorName'})
        commenter_name = str(commenter.contents[0])
        commenter_href = str(commenter['href'])

        if commenter_name not in authors:
            authors[commenter_name] = author_id, commenter_href
            current_id = author_id
            author_id += 1
        if commenter_name in authors: 
            current_id = authors[commenter_name][0]

        # Write the author tag
        output.write('<author id="'+str(current_id)+'" \
                idref="'+com_idref+'" url="'\
                +commenter_href+'">')
        output.write(commenter_name)
        output.write('</author>')

        # Find the time
        time = comment.find('abbr')
        utime = time['data-utime']
        time_readable = time['title']

        # Write the timestamp tag
        output.write('<timestamp idref="'+com_idref+\
                '" utime="'+str(utime)+'">')
        output.write(time_readable)
        output.write('</timestamp>')

        # Find if it was liked
        likes = comment.find('span', {'data-ft': \
                '{"type":36}'}).find('a')
        if likes != None:
            like_id += 1
            likes = likes.contents[1]

            output.write('<likes id="'+com_idref+'.'+\
                    str(like_id)+'" idref="'+com_idref+'">')
            output.write('<likes_total idref="'+\
                    com_idref+'.'+str(like_id)+'">')
            output.write(likes)
            output.write('</likes_total>')
            output.write('</likes>')

        # Done on a mobile?
        mobile = comment.find('a', {'class': 'uiLinkSubtle'})
        if mobile != None:
            mobile = mobile.contents[0]

            output.write('<source id="'+str(source_id)+\
                    '" idref="'+com_idref+'">')
            output.write(mobile)
            output.write('</source>')

            source_id += 1

        # Find the comment
        message = comment.find('span', {'class': 'commentBody'}).contents

        # This removes all tags. It does handle the data,
        # But makes text much easier to get.
        for x in range(len(message)):
            message[x] = re.sub(r'<.*>', '', str(message[x]))
        message = ' '.join(message)

        output.write('<plaintext idref="'+com_idref+'">')
        output.write(message)
        output.write('</plaintext>')

        ## Phrase id, word id needs to be done. 

        output.write('</comment>')
    output.write('</thread>')

output.write('</body>')
output.write('</text>')

output.close()

# Let's make that output pretty, shall we? Why not.

pretty = 'file:///Users/richardlittauer/Documents/Research/Topics/Rangi/output_raw'
output_file_name = 'output_pretty.xml'
output = open(output_file_name,'w+')
u = urllib2.urlopen(pretty)

# mung it all together
rawhtml = "".join(map(str.strip,u.readlines()))
bs = BeautifulSoup(rawhtml)
output.write(bs.prettify())
output.close()

# <!-- Incorporate Rangi end word of joy! -->
