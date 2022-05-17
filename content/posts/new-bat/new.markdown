Title: winsows效率之bat文件1
Date: 2022-05-14
Category: 效率
Tags: bat
Slug: new-bat
Author: lart
Status: published


    :::c
    spx_private err_t spx_map_expand(struct spx_map *map);

    spx_private err_t spx_map_expand(struct spx_map *map){
        err_t err = 0;
        size_t slots_count = (size_t) map->slots_count * SpxMapFactor;
        struct spx_map_slot *newslot = spx_alloc_alone(\
                sizeof(*newslot) * slots_count,&err);
        if(NULL == newslot){
            return err;
        }

        struct spx_map_key_node *knode = map->keys_header;
        while(NULL != knode){
            struct spx_map_node *n = knode->node;
            size_t idx = n->hash % slots_count;
            struct spx_map_slot *s = newslot + idx;
            if(NULL == s->header){
                s->header = n;
                s->tail = n;
            } else {
                n->prev = s->tail;
                s->tail->next = n;
                s->tail = n;
            }
            s->real_size ++;
            knode = knode->next;
        }

        SpxFree(map->slots);
        map->slots = newslot;
        map->slots_count = slots_count;
        return err;
    }

    struct spx_map *spx_map_new(SpxLogDelegate *log,\
            SpxCollectionKeyHashDelegate *hash,\
            SpxCollectionCmperDelegate *cmper,\
        SpxCollectionKeyPrintfDelegate *kprintf,\
        SpxCollectionKeyFreeDelegate *kfree,\
        SpxCollectionValueFreeDelegate *vfree,\
        err_t *err){
        struct spx_map *map = spx_alloc_alone(sizeof(*map),err);
        if(NULL == map){
            SpxLog2(log,SpxLogError,*err,"alloc map is fail.");
            return NULL;
        }

        map->slots = spx_alloc_alone(sizeof(*(map->slots)) * SpxMapSlotSize,err);
        if(NULL == map->slots){
            goto r1;
        }
        map->slots_count = SpxMapSlotSize;
        map->hash = hash;
        map->vfree = vfree;
        map->kprintf = kprintf;
        map->kfree = kfree;
        map->cmper = cmper;
        map->log = log;
        return map;
    r1:
        SpxFree(map->slots);
        SpxFree(map);
        return NULL;
    }

@eche off
@title 本地预览pelican博客

echo 进入文件夹
rem 这是我的content所在目录
cd /d D:\git clone\BLOG\lart\lart

echo 执行pelican content
pelican content

echo 进入output
cd /d output

echo 启动本地服务器
python -m pelican.server

echo 结束...
echo 请前往 http://localhost:8000/ 查看
pause

