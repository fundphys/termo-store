def jsonify_data(data, controller_type, controller_ip):
    if controller_type == "PET7015":
        if controller_ip == "192.168.15.71":
            return [{
                        "measurement": "raw",
                        "tags": {
                            "controller": controller_type,
                            "controller_ip": controller_ip,
                        },
                        "time": data.ch_1.index[0],
                        "fields": {
                                "ch_1": data.ch_1[0],
                                "ch_2": data.ch_2[0],
                                "ch_3": data.ch_3[0],
                                "ch_4": data.ch_4[0],
                                "ch_5": data.ch_5[0],
                                "ch_6": data.ch_6[0],
                                "ch_7": data.ch_7[0],
                        }
                    },
                    {
                        "measurement": "temperature",
                        "tags": {
                            "controller": controller_type,
                            "controller_ip": controller_ip,
                        },
                        "time": data.ch_1.index[0],
                        "fields": {
                                "t1": data.ch_1[0] * 0.018497 + 0.14152,
                                "t2": data.ch_2[0] * 0.018273 + 0.2538,
                                "t3": data.ch_3[0] * 0.018476 + 0.48769,
                                "t4": 0 * data.ch_4[0] * 0.018571 + 0.63772,
                                "t5": data.ch_5[0] * 0.018561 +  0.47769,
                                "t6": data.ch_6[0] * 0,
                                "t7": data.ch_7[0] * 0.018556 + -0.062518
                        }
                    },
                    ]

        elif controller_ip == "192.168.15.72":
            pass

        else:
            print("Unknown IP addres of controller")
            return None

    elif controller_type == "CHINA":
        return [{
            "measurement": "raw",
            "tags": {
                "controller": controller_type,
                "controller_ip": controller_ip,
            },
            "time": data.ch_1.index[0],
            "fields": {
                "ch_1": data.ch_01[0],
                "ch_2": data.ch_02[0],
                "ch_3": data.ch_03[0],
                "ch_4": data.ch_04[0],
                "ch_5": data.ch_05[0],
                "ch_6": data.ch_06[0],
                "ch_7": data.ch_07[0],
                "ch_8": data.ch_08[0],
                "ch_9": data.ch_09[0],
                "ch_10": data.ch_10[0],
                "ch_11": data.ch_11[0],
                "ch_12": data.ch_12[0],
            }
        }]

    else:
        print("unknown type of controller!")
        return None