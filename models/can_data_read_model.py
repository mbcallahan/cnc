
class MyBehaviorModel:
    relevant_inputs = []
    relevant_outputs = [
        'TX'
    ]

    def validate(self, inputs, outputs):
        """Returns whether the signals represent correct operation of the device"""
        tx = self.relevant_output_values[0].signal

        #print("Data changes: ", list(tx.changes()))

        changes = list(tx.changes())
        t_start = list()
        t_stop = list()
        index=0
        count = 0
        for c in changes:
            if (c[1] == 1):
                if tx.value_at_time(c[0] + 0.22/1000) == 1:
                    if changes[index+1][0] > (c[0]+0.22/1000):
                        t_start.append(index+1)
                        t_stop.append(index)
                        count += 1
                    if count == 2:
                        break
            index += 1

        msg_times = list()
        for i in range(0,len(t_start)-1):
            msg_times.append([t_start[i],t_stop[i+1]])

        msgs = list()
        first_c = msg_times[0][0]
        bit_time = changes[first_c+1][0] - changes[first_c][0]
        for i in range(0,len(msg_times)):
            msg = list()
            for j in range(msg_times[i][0], msg_times[i][1]):
                cur_bit = changes[j][0]
                nxt_bit = changes[j+1][0]
                for k in range(0,round((nxt_bit-cur_bit)/bit_time)):
                    msg.append(changes[j][1])
            msgs.append(msg)
            print("TX msg: ", msg)
            
ModelClass = MyBehaviorModel
