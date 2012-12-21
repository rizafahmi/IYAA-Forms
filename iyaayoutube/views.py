from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import threading


threads = []
# @view_config(route_name='home', renderer='index.html')
# def my_view(request):
#     return {'project': 'IyaaYoutube'}
#


@view_config(route_name='home', renderer='index.html')
def save_view(request):
    if request.POST:
        import datetime
        new_data = {
            'nama': request.POST['inputNama'],
            'email': request.POST['inputEmail'],
            'phone': request.POST['inputPhone'],
            'tiket1': request.POST['inputTiket1'],
            'tiket2': request.POST['inputTiket2'],
            'tiket3': request.POST['inputTiket3'],
            'tiket4': request.POST['inputTiket4'],
            'tiket5': request.POST['inputTiket5'],
            'tgl': datetime.datetime.now(),
        }

        if new_data:
            request.db['musicbank_early'].save(new_data)
            print "SAVE DATA"
            print new_data
            # send_email(new_data)
            t = threading.Thread(target=send_email, args=(new_data['nama'], new_data['email'],
                new_data['phone'], new_data['tiket1'], new_data['tiket2'], new_data['tiket3'], new_data['tiket4'],
                new_data['tiket5']))

            threads.append(t)
            t.start()
            # return HTTPFound(location='http://www.iyaa.com/hiburan/musik/musicbank/pre2.html')
    return {}


def send_email(*data):
    print "sending email..."
    import smtplib

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()
    gmail_user = "musicbank@iyaa.com"

    msg['From'] = gmail_user
    msg['To'] = data[1]
    msg['Subject'] = "MUSIC BANK - Konfirmasi Tiket Prebooking"

    # html = "<h1>Thanks for pre-booking, " + data[0] + "</h1>"
    # html = html + "Info: <br />"
    # html = html + tiket1 + "<br />"
    # html = html + tiket2 + "<br />"
    # html = html + tiket3 + "<br />"
    # html = html + tiket4 + "<br />"
    # html = html + tiket5 + "<br />"

    html = """\
                    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>IYAA email confirmation</title>
<style>
.konfirmasi{
background-color:#BBC832;
color:#fff;
font-size:13px;
line-height:120%;
padding:10px 30px;
font-family:Verdana;
font-weight:bold;
    }

.konfirmasi a{

color:#fff;
font-size:13px;
line-height:120%;

font-family:Verdana;
font-weight:bold;
text-decoration:none;
    }


</style>
</head>

<body>
<table width="700" border="0" align="center" cellspacing="0" style="border:1px solid #C1C1C1;padding:10px;">
  <tr>
    <td colspan="6" style="padding:30px 0 30px 26px;"><img src="http://www.iyaa.com/images/iyaa_logo_email.png" width="100" height="50" /></td>
  </tr>
  <tr>
    <td height="93" colspan="6" style="padding:0px 26px 0px 26px;font-family:Verdana;color:#999;text-align:left;text-decoration:none;font-size:12px;line-height:185%;">Selamat! Anda telah memastikan akan menonton Music Bank!
    </br>
    Berikut ini adalah detail tiket yang telah Anda pesan:<br />
    Nama: """
    html = html + data[0] + "<br />"
    import datetime
    dt = datetime.datetime.now()

    html = html + "Tanggal: " + str(dt.strftime("%d %b %Y"))
    html = html + "<br />DIAMOND: " + data[3]
    html = html + "<br />GOLD: " + data[4]
    html = html + "<br />SILVER: " + data[5]
    html = html + "<br />BRONZE: " + data[6]
    html = html + "<br />FESTIVAL: " + data[7]
    html = html + """\
        <br /><br /><br />Selanjutnya, Pihak D Market selaku official ticket box untuk Music Bank akan menghubungi Anda dengan jadwal sebagai berikut:<br />
        <ul>
        <li>26 Desember 2012 ~ 3 Januari 2013: Anda akan menerima email dari Dmarket dengan nomor pemesanan untuk membeli tiket.</li>
        <li>26 Desember 2012 ~ 3 Januari 2013: Setelah mendapat email, Anda dapat langsung melakukan pembelian.</li>
        <li>9 Maret 2013: Selamat menonton Music Bank!</li>
        </ul>
        <br />
        Setelah Anda melakukan pre-booking, Anda tidak bisa mengganti jenis tiket atau jumlah tiket saat Anda melakukan pembelian. Anda akan menerima voucher online dari Dmarket via email yang Anda daftarkan setelah Anda menyelesaikan pembelian. Anda perlu membawa email ini saat konser Music Bank dan menukarnya dengan tiket. <br />
        <br />

        Salam,<br /><br />
        <a href="http://www.iyaa.com/">IYAA.COM</a><br /><br />
        Email ini dikirim secara otomatis oleh komputer. Harap tidak membalas pada email ini. Untuk informasi lebih lanjut, harap hubungi Dmarket: musicbank@dmarket.co.id atau 021-5210598
    </td>
  </tr>

</table>

<table width="700" border="0" align="center" cellspacing="0" >
  <tr >
    <td width="88"  bgcolor="#48C2C3"><img src="http://www.iyaa.com/images/iyaa_footer_email.png" width="2" height="9" /></td>
    <td width="23"  bgcolor="#0873BA"></td>
    <td width="109"  bgcolor="#60BB46"></td>
    <td width="211" bgcolor="#BBC831"></td>
    <td width="54" bgcolor="#48C2C3"></td>
    <td width="203"  bgcolor="#0873BA"></td>
  </tr>
</table>
</body>
</html>
"""

    msg.attach(MIMEText(html, 'html'))

    import pymongo
    import datetime
    conn = pymongo.Connection(host="mongo.iyaa.com", port=5858)
    mongo = conn.iyaa

    try:
        mailServer = smtplib.SMTP("smtp.ionsoft.co.id", 25)
        mailServer.ehlo()
        # mailServer.starttls()
        gmail_pwd = 'abcde12#'
        mailServer.login(gmail_user, gmail_pwd)
        mailServer.sendmail("musicbank@iyaa.com", data[1], msg.as_string())
        mailServer.close()
        print "EMAIL Sent to: " + str(data[1])

        data_email = {'email': str(data[1]),
                'status': 'sent',
                'tgl': str(datetime.datetime.now()),
                }
        mongo['musicbank_early_email'].save(data_email)
    except Exception, e:
        data_email = {'email': str(data[1]),
                'status': str(e),
                'tgl': str(datetime.datetime.now()),
                }
        mongo['musicbank_early_email'].save(data_email)
        print "Enable to send email. Error: %s" % str(e)


@view_config(route_name='form', renderer='index.html')
def form_view(request):
    if request.POST:
        new_data = {
            'nama': request.POST['inputNama'],
            'email': request.POST['inputEmail'],
            'phone': request.POST['inputPhone'],
            'tiket1': request.POST['inputTiket1'],
            'tiket2': request.POST['inputTiket2'],
            'tiket3': request.POST['inputTiket3'],
            'tiket4': request.POST['inputTiket4'],
            'tiket5': request.POST['inputTiket5'],
        }

        if request.POST['inputNama']:
            request.db['musicbank_early'].save(new_data)
            import smtplib

            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            msg = MIMEMultipart()
            gmail_user = "musicbank@iyaa.com"

            msg['From'] = gmail_user
            msg['To'] = request.POST['inputEmail']
            msg['Subject'] = "MUSIC BANK - Konfirmasi Tiket Prebooking"

            html = "<h1>Thanks for pre-booking, " + request.POST['inputNama'] + "</h1>"
            html = html + "Info: <br />"
            html = html + request.POST['inputPhone'] + "<br />"
            html = html + request.POST['inputTiket1'] + "<br />"
            html = html + request.POST['inputTiket2'] + "<br />"
            html = html + request.POST['inputTiket3'] + "<br />"
            html = html + request.POST['inputTiket4'] + "<br />"
            html = html + request.POST['inputTiket5'] + "<br />"

            html = """\
                    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>IYAA email confirmation</title>
<style>
.konfirmasi{
background-color:#BBC832;
color:#fff;
font-size:13px;
line-height:120%;
padding:10px 30px;
font-family:Verdana;
font-weight:bold;
    }

.konfirmasi a{

color:#fff;
font-size:13px;
line-height:120%;

font-family:Verdana;
font-weight:bold;
text-decoration:none;
    }


</style>
</head>

<body>
<table width="700" border="0" align="center" cellspacing="0" style="border:1px solid #C1C1C1;padding:10px;">
  <tr>
    <td colspan="6" style="padding:30px 0 30px 26px;"><img src="http://www.iyaa.com/images/iyaa_logo_email.png" width="100" height="50" /></td>
  </tr>
  <tr>
    <td height="93" colspan="6" style="padding:0px 26px 0px 26px;font-family:Verdana;color:#999;text-align:left;text-decoration:none;font-size:12px;line-height:185%;">Selamat! Anda telah memastikan akan menonton Music Bank!
    </br>
    Berikut ini adalah detail tiket yang telah Anda pesan:<br />
    Nama: """
            html = html + request.POST['inputNama'] + "<br />"
            import datetime
            dt = datetime.datetime.now()

            html = html + "Tanggal: " + str(dt.strftime("%d %b %Y"))
            html = html + "<br />DIAMOND: " + request.POST['inputTiket1']
            html = html + "<br />GOLD: " + request.POST['inputTiket2']
            html = html + "<br />SILVER: " + request.POST['inputTiket3']
            html = html + "<br />BRONZE: " + request.POST['inputTiket4']
            html = html + "<br />FESTIVAL: " + request.POST['inputTiket5']
            html = html + """\
        <br /><br /><br />Selanjutnya, Pihak D Market selaku official ticket box untuk Music Bank akan menghubungi Anda dengan jadwal sebagai berikut:<br />
        <ul>
        <li>26 Desember 2012 ~ 3 Januari 2013: Anda akan menerima email dari Dmarket dengan nomor pemesanan untuk membeli tiket.</li>
        <li>26 Desember 2012 ~ 3 Januari 2013: Setelah mendapat email, Anda dapat langsung melakukan pembelian.</li>
        <li>9 Maret 2013: Selamat menonton Music Bank!</li>
        </ul>
        <br />
        Setelah Anda melakukan pre-booking, Anda tidak bisa mengganti jenis tiket atau jumlah tiket saat Anda melakukan pembelian. Anda akan menerima voucher online dari Dmarket via email yang Anda daftarkan setelah Anda menyelesaikan pembelian. Anda perlu membawa email ini saat konser Music Bank dan menukarnya dengan tiket. <br />
        <br />

        Salam,<br /><br />
        <a href="http://www.iyaa.com/">IYAA.COM</a><br /><br />
        Email ini dikirim secara otomatis oleh komputer. Harap tidak membalas pada email ini. Untuk informasi lebih lanjut, harap hubungi Dmarket (Ulfi): ulfi@dmarket.co.id atau 021-5210598
    </td>
  </tr>

</table>

<table width="700" border="0" align="center" cellspacing="0" >
  <tr >
    <td width="88"  bgcolor="#48C2C3"><img src="http://www.iyaa.com/images/iyaa_footer_email.png" width="2" height="9" /></td>
    <td width="23"  bgcolor="#0873BA"></td>
    <td width="109"  bgcolor="#60BB46"></td>
    <td width="211" bgcolor="#BBC831"></td>
    <td width="54" bgcolor="#48C2C3"></td>
    <td width="203"  bgcolor="#0873BA"></td>
  </tr>
</table>
</body>
</html>
"""

            msg.attach(MIMEText(html, 'html'))

            mailServer = smtplib.SMTP("smtp.ionsoft.co.id", 25)
            mailServer.ehlo()
            # mailServer.starttls()
            # mailServer.login(gmail_user, gmail_pwd)
            mailServer.sendmail("IYAA.COM <musicbank@iyaa.com>", request.POST['inputEmail'], msg.as_string())
            mailServer.close()

            return HTTPFound(eocation='http://www.iyaa.com/hiburan/musik/musicbank/pre2.html')
    return {}


@view_config(route_name='countdown', renderer='countdown.html')
def countdown_view(request):
    return {}


@view_config(route_name='list', renderer='list.html')
def list_view(request):
    allow = ['202.77.101.34', '192.168.103.2', '202.77.102.30']
    if request.remote_addr in allow:
        # data = request.db['musicbank_early'].find({'tiket5': {'$exists': False}}).sort('phone', -1)
        # data = request.db['musicbank_early'].find({'tiket5': {'$exists': True}})
        # data2 = request.db['musicbank_early'].find({'tiket5': {'$exists': True}})
        data = request.db['musicbank_early'].find()
        data2 = request.db['musicbank_early'].find()

        total_1 = 0
        total_2 = 0
        total_3 = 0
        total_4 = 0
        total_5 = 0
        for d in data2:
            if d['tiket1']:
                total_1 = total_1 + int(d['tiket1'])
            if d['tiket1']:
                total_2 = total_2 + int(d['tiket2'])
            if d['tiket1']:
                total_3 = total_3 + int(d['tiket3'])
            if d['tiket1']:
                total_4 = total_4 + int(d['tiket4'])
            if d.get('tiket5', None):
                total_5 = total_5 + int(d['tiket5'])

        return {'users': data,
                'total_1': total_1,
                'total_2': total_2,
                'total_3': total_3,
                'total_4': total_4,
                'total_5': total_5,

                }
    else:
        return HTTPFound(location='noaccess')


@view_config(route_name='pilih', renderer='pilih.html')
def pilih_view(request):

    return {}


@view_config(route_name='noaccess', renderer='noaccess.html')
def noaccess_view(request):

    return {}


@view_config(route_name='email_list', renderer='email_list.html')
def email_view(request):
    allow = ['202.77.101.34', '192.168.103.2', '202.77.102.30']
    if request.remote_addr in allow:
        import pymongo
        conn = pymongo.Connection(host="mongo.iyaa.com", port=5858)
        mongo = conn.iyaa
        data = mongo['musicbank_early_email'].find()

        return {'data': data}
    else:
        return HTTPFound(location='noaccess')
