from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound


# @view_config(route_name='home', renderer='index.html')
# def my_view(request):
#     return {'project': 'IyaaYoutube'}
#

@view_config(route_name='home', renderer='index.html')
def save_view(request):
    if request.POST:
        new_data = {
            'nama': request.POST['inputNama'],
            'email': request.POST['inputEmail'],
            'phone': request.POST['inputPhone'],
            'tiket1': request.POST['inputTiket1'],
            'tiket2': request.POST['inputTiket2'],
            'tiket3': request.POST['inputTiket3'],
            'tiket4': request.POST['inputTiket4'],
        }
        print request.POST
        if request.POST['inputNama']:
            request.db['musicbank_early'].save(new_data)
            return HTTPFound(location='http://www.iyaa.com/hiburan/musik/musicbank/early2.html')
    return {'message': 'Silakan isi nama kamu.<br /><a href="http://www.iyaa.com:6540/">Halaman sebelumnya.</a>'}


@view_config(route_name='coverdance', renderer='coverdance.html')
def coverdance_view(request):
    return {}


@view_config(route_name='save_coverdance', renderer='save.html')
def save_coverdance_view(request):
    import re
    if request.POST:
        data = request.db['wondergirls_coverdance'].find({'nama': request.POST['inputNamaGroup']}).count()
        if data < 1:
            video_id = ''
            match = re.search(r'http://(?:www\.)?youtu(?:be\.com/watch\?v=|\.be/)([\w-]*)(&(amp;)?[\w\?=]*)?', request.POST['inputLink'])
            if match:
                video_id = match.group(1)
            else:
                video_id = 'id not found'
                return {'message': 'Maaf, URL yang Anda masukkan keliru. Mohon masukkan link video Youtube kamu. <a href="http://www.iyaa.com:6540/coverdance">Halaman sebelumnya.</a>'}

            new_data = {
                'nama': request.POST['inputNamaGroup'],
                'link': request.POST['inputLink'],
                'video_id': video_id,
            }

            if request.POST['inputNamaGroup'] and request.POST['inputLink']:
                request.db['wondergirls_coverdance'].save(new_data)
        else:
            return{'message': 'Nama group sudah terdaftar. Silakan masukkan nama lainnya jika kamu belum pernah mendaftar. \
                    <br /><a href="http://www.iyaa.com:6540/coverdance">Halaman sebelumnya.</a>'}

    return {'message': 'Terima kasih atas partisipasi kamu! Cek video kamu dan kontestan lainnya di <a href="http://www.iyaa.com/hiburan/musik/wondergirls/kontestancoverdance/kontestan_coverdance.html" target="_blank">sini.</a>'}


@view_config(route_name='list', renderer='list.html')
def list_view(request):
    import simplejson
    import urllib

    data = request.db['wondergirls_coverdance'].find().sort('_id', -1)

    newest_url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % data[0]['video_id']
    newest_json = simplejson.load(urllib.urlopen(newest_url))

    return {'main_video': data, 'title': newest_json['entry']['title']['$t'],
        'author': newest_json['entry']['author'][0]['name']['$t'],
        }


@view_config(route_name='view_video', renderer='view_video.html')
def view_video(request):
    import simplejson
    import urllib

    url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % request.matchdict['video_id']
    json = simplejson.load(urllib.urlopen(url))

    data = request.db['wondergirls_coverdance'].find({'video_id': {'$ne': request.matchdict['video_id']}}).sort('_id', -1)
    return {'main_video': data, 'title': json['entry']['title']['$t'], 'author': json['entry']['author'][0]['name']['$t']}


@view_config(route_name='flashlist', renderer='flashlist.html')
def flashlist(request):
    data = request.db['wondergirls_flashmob'].find().sort('_id', -1)

    return {'title': 'Flashmob', 'users': data}


@view_config(route_name='coverlist', renderer='coverlist.html')
def coverlist(request):
    data = request.db['wondergirls_coverdance'].find().sort('_id', -1)

    return {'title': 'Cover Dance', 'users': data}


@view_config(route_name='delete')
def delete_view(request):
    from pyramid.httpexceptions import HTTPFound
    import bson

    request.db['wondergirls_coverdance'].remove({"_id": bson.ObjectId(request.matchdict['id'])})

    return HTTPFound(location=request.route_url('coverlist'))
