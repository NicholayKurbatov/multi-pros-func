===================================================================================
МНОГОПОТОЧНОСТЬ
===================================================================================
pbar = tqdm(total=len(result))

    def update(out):
        pbar.update()

    pool = mp.Pool(n_jobs)  # открываем процессы
    need_func = partial(async_load_find,
                        path_frames=path_frames,
                        false_idx=false_idx,
                        loc_x_start=loc_x_start,
                        loc_x_end=loc_x_end,
                        num_brightpixels=num_brightpixels)

    for name_frame in sorted(result):
        pool.apply_async(need_func, args=(name_frame, ), callback=update)

    pool.close()
    pool.join()
    pbar.close()


===============================================================
еще вариант
===============================================================
    s3_task = lambda x: reader_csv(container_name=container_name, key_name=x, is_header=is_header)
    # if use concurrent reading 
    data = []
    if concurr:
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(s3_task, f) for f in obj_list]
            for s3_thread in as_completed(futures):
                data += [s3_thread.result()]

================================================================
еще
================================================================

with ThreadPoolExecutor(max_workers=num_workers) as executor:
    futures = list(tqdm(executor.map(parse_fun, list_blobs), total=len(list_blobs)))
