def jsonify_data(data, controller_type, controller_ip):
    if controller_type == "PET7015":
        if controller_ip == "192.168.15.71":
            return [{
                        "measurement": "temperatures",
                        "tags": {
                            "controller": controller_type,
                            "controller_ip": controller_ip,
                            "location": "dome",
                            "medium": "air",
                            "channel": 1 
                        },
                        "time": data.ch_1.index[0],
                        "fields": {
                            "data": data.ch_1[0],
                            "temperture": 0.018497 * data.ch_1[0] + 0.14152
                        },
                    },
                    {
                        "measurement": "temperatures",
                        "tags": {
                            "controller": controller_type,
                            "controller_ip": controller_ip,
                            "location": "dome",
                            "medium": "air",
                            "channel": 2
                        },
                        "time": data.ch_1.index[0],
                        "fields": {
                            "data": data.ch_2[0],
                            "temperture": 0.018273 * data.ch_2[0] + 0.2538
                        },
                    },

                    ]

        elif controller_ip == "192.168.15.72":
            pass

        else:
            print("Unknown IP addres of controller")
            return None

    elif controller_type == "CHINA":
        pass

    else:
        print("unknown type of controller!")
        return None