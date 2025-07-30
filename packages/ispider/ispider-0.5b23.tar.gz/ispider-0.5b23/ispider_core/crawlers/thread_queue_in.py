import time
import random
import multiprocessing as mp
from queue import Empty  # Import to catch queue exceptions

from ispider_core.utils import queues
from ispider_core.utils import ifiles

from ispider_core.utils.logger import LoggerFactory

def queue_in_srv(
    script_controller, dom_stats, 
    seen_filter, conf, qin, qout):
    
    logger = LoggerFactory.create_logger(conf, "ispider.log", stdout_flag=True)
    
    Q_MAX = conf['QUEUE_MAX_SIZE']
    Q_BLOCK_MAX = max(min(Q_MAX, 5000), Q_MAX // 2)
    Q_BLOCK_MIN = max(min(Q_MAX, 1000), Q_MAX // 10)

    to_insert = []

    logger.debug("Begin Queue Process")
    
    t0 = time.time()

    try:
        while True:
            # logger.info("QueueIN Cycle")
            if time.time() - t0 > 5:
                if script_controller['running_state'] == 0:
                    logger.info("Closing queue_in_srv")
                    break
                t0 = time.time()

            reqA = None
            if not qout.empty():
                try:
                    reqA = qout.get(timeout=1)

                    #--------------------
                    # Verify if in seen
                    if seen_filter.req_in_seen(reqA):
                        dom_stats.reduce_missing(reqA[2])
                        dom_stats.reduce_total(reqA[2])
                        continue
                    #--------------------
                except Empty:
                    pass
            

            if reqA is not None:
                to_insert.append(reqA)

            if len(to_insert) < Q_BLOCK_MIN and qout.empty():
                # logger.debug(f"Qwait case 1 --> INS: {len(to_insert)} -- BLOCK: {Q_BLOCK_MIN} -- OUT: {qout.qsize()} -- IN: {qin.qsize()}")
                time.sleep(.5)  # Lower sleep time for responsiveness

            if len(to_insert) >= Q_BLOCK_MAX or qout.empty():
                while qin.qsize() >= Q_MAX // 2:
                    time.sleep(2)

                # Ensure function exists before calling
                to_insert = queues.sparse_q_elements(to_insert)

                for el in to_insert:
                    seen_filter.add_to_seen_req(el)
                    qin.put(el)

                to_insert.clear()


    except KeyboardInterrupt:
        logger.warning(f"Keyboard Interrupt received. Missing to insert: {len(to_insert)}")
        logger.warning("Keyboard Interrupt received. Closing the q_in queue manager")
    except Exception as e:
        logger.fatal(f"Fatal error in qproc: {e}")
