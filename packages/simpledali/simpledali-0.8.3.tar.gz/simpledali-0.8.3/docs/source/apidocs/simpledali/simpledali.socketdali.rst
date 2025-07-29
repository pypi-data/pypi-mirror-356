:py:mod:`simpledali.socketdali`
===============================

.. py:module:: simpledali.socketdali

.. autodoc2-docstring:: simpledali.socketdali
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`SocketDataLink <simpledali.socketdali.SocketDataLink>`
     - .. autodoc2-docstring:: simpledali.socketdali.SocketDataLink
          :summary:

API
~~~

.. py:class:: SocketDataLink(host, port, packet_size=-1, dlproto=DLPROTO_1_0, verbose=False)
   :canonical: simpledali.socketdali.SocketDataLink

   Bases: :py:obj:`simpledali.abstractdali.DataLink`

   .. autodoc2-docstring:: simpledali.socketdali.SocketDataLink

   .. rubric:: Initialization

   .. autodoc2-docstring:: simpledali.socketdali.SocketDataLink.__init__

   .. py:method:: createDaliConnection()
      :canonical: simpledali.socketdali.SocketDataLink.createDaliConnection
      :async:

      .. autodoc2-docstring:: simpledali.socketdali.SocketDataLink.createDaliConnection

   .. py:method:: send(header, data)
      :canonical: simpledali.socketdali.SocketDataLink.send
      :async:

      .. autodoc2-docstring:: simpledali.socketdali.SocketDataLink.send

   .. py:method:: parseResponse()
      :canonical: simpledali.socketdali.SocketDataLink.parseResponse
      :async:

      .. autodoc2-docstring:: simpledali.socketdali.SocketDataLink.parseResponse

   .. py:method:: isClosed()
      :canonical: simpledali.socketdali.SocketDataLink.isClosed

      .. autodoc2-docstring:: simpledali.socketdali.SocketDataLink.isClosed

   .. py:method:: close()
      :canonical: simpledali.socketdali.SocketDataLink.close
      :async:

   .. py:method:: _force_close()
      :canonical: simpledali.socketdali.SocketDataLink._force_close
