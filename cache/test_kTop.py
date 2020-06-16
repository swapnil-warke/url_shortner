from url_shortner.temp_snips.kTopUrl import KTopUrl, ConstKTop


def test_1():
    kt = KTopUrl(5)


    kt.add_url('12345678')
    kt.add_url('abcdefgh')
    kt.add_url('mnopqrst')


    kt.add_url('swswswsw')
    kt.add_url('lslslsls')
    kt.add_url('lslslsls')
    kt.add_url('12345678')
    kt.add_url('12345678')

    kt.add_url('abcdefgh')
    kt.add_url('abcdefgh')
    kt.add_url('abcdefgh')
    kt.add_url('abcdefgh')

    kt.add_url('mnopqrst')
    kt.add_url('12345678')
    kt.add_url('12345678')
    kt.add_url('abcdefgh')
    l=kt.get_topK_urls()

    sol_list = ['abcdefgh', '12345678', 'mnopqrst', 'lslslsls', 'swswswsw']



     for i in range(5):
        assert l[i] == sol_list[i], 'solution incorrect'


