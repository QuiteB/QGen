            a=0
            b=0
            for ni in p_json:
                for ni2 in p_jsonl:
                    if usernamesl[a]==usernames[b]:
                        fnames.append(p_jsonl[a]['fname'])
                        lnames.append(p_jsonl[a]['lname'])
                    a+=1
                b+=1