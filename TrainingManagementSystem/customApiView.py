from rest_framework.views import APIView


class CAPIView(APIView):
    _keys = ['status', 'message', 'data']

    def finalize_response(self, request, response, *args, **kwargs):
        """强制统一接口返回格式:
            {
                "status": 0,
                "errmsg": 'success',
                "data": '',
            }
        """

        data = response.data
        status_code = response.status_code

        # 如果response.data不合法，规范成一个合法字典
        if not isinstance(data, dict):
            response.data = {
                "status": status_code,
                "errmsg": 'success',
                "data": response.data,
            }
        elif not set(data.keys()) == set(self._keys):
            # success: 200~299
            result = (200 <= status_code <= 299)

            if result:
                message = data.get('message', 'success')
            else:
                message = data.get('_err_msg', data.get('detail', 'failed'))
                data.pop('_err_msg', None)

            response.data = {
                "status": status_code,
                "errmsg": message,
                "data": response.data,
            }

        return super(CAPIView, self).finalize_response(
            request, response, *args, **kwargs
        )
