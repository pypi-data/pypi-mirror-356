from camagick.processor import ProcessorBase, SinkBase

## Data sink to store (append) stuff in a HDF5 DataArray

import numpy as np
import h5py, logging, os, random, time

logger = logging.getLogger(__name__)

class RefuseIndex(RuntimeError): pass

class RefuseOverwrite(RefuseIndex): pass

class RefuseSparse(RefuseIndex): pass


class Hdf5DataStacker:
    '''
    Simple HDF5 stacking-based storage.
    '''
    
    
    def __init__(self, h5file, h5group=None, mode=None):
        '''
        Args:
            h5file: HDF5 file name to store data in.
        
            h5group: Group path _inside_ the HDF5 file where to save the data.

            mode: What to do when we're required to save a data point
              in a dataset for which there's already data available
              in the same dataset. See `Processor.__init__()` for documentation
              on available modes.
        '''
        self._h5file = h5file
        self._h5group = h5group if h5group is not None else '/'

        self._frame_mode = mode if mode is not None else 'a+'


    def _h5obj(self, init=True):
        return h5py.File(self._h5file, 'a')


    def _ensure_group(self, h5, nodepath):
        # Makes sure `nodepath` exists in the current h5 file and is a data group

        subpath = ""
        subnode = h5
        for current in nodepath.split('/'):

            if len(current) == 0:
                continue # nothing to do

            try:
                subnode = subnode[current]
            except KeyError:
                logger.info(f'msg="Creating node" file="{subnode.filename}" '
                            f'parent="{subnode.name}" '
                            f'name="{current}"')
                node = subnode.create_group(current)


    def _dtype_spec_to_dtype(self, ds):
        if isinstance(ds, str):
            try:            
                return {
                    'number': float,
                    'integer': int,
                    'array': float,
                }[ds]
            except KeyError:
                errmsg = f'tag="{key}" msg="Don\'t know how to save" dtype="{dt_spec}"'
                logger.error(errmsg)
                raise RuntimeError(errmsg)

        else:
            return ds


    def _ensure_dataset(self, grpobj, name, dtype, point_shape):
        '''
        Received with the first data point, sets names, types etc.

        Args:
            grpobj: HDF5 group object
            name: name of the dataset
            dtype: data type (numpy-dtype)
            point_shape: shape of the data point; note that
              the actual shape of the resulting data set will contain
              more dimension
        '''

        dshape = (0, *point_shape)
        
        try:
            dset = grpobj[name]

            if (dset.dtype != dtype):
                if  'O' not in self._frame_mode:
                    raise RuntimeError(f'msg="Dataset exists with different dtype"'
                                       f'have="{dset.dtype}" want="{dtype}"')
                else:
                    del grpobj[name]
                    raise KeyError()

            if dset.shape[1:] != dshape[1:]:
                if  'O' not in self._frame_mode:                
                    raise RuntimeError(f'msg="Dataset exists with different shape"'
                                       f'have="{dset.shape}" want="{dshape}"')
                else:
                    del grpobj[name]
                    raise KeyError()

        except KeyError:
            logger.info(f'msg="Creating dataset" file="{grpobj.file.filename}" name="{name}" '
                        f'shape="{dshape}" dtype={dtype}')
            grpobj.create_dataset(name, dshape, maxshape=(None, *dshape[1:]),
                                  dtype=dtype, compression='lzf')


    def _ensure_frame(self, dset, index, fname=None):
        
        idiff = (index-dset.shape[0]) + 1

        if fname is None:
            fname = dset.file.filename
        
        if idiff == 1:
            shape_diff = 1
            
        elif idiff > 1:
            if '+' in self._frame_mode:
                shape_diff = idiff
            else:
                raise RefuseSparse(f'msg="Sparse writing not allowed; use top-up `+` flag" '
                                   f'file={fname} '
                                   f'index={index} frames={dset.shape[0]} dataset="{dset.name}"')
            
        elif idiff <= 0:
            if 'a' in self._frame_mode:
                raise RefuseOverwrite(f'msg="Overwrite not permitted" index={index} '
                                      f'file={fname} '
                                      f'frames={dset.shape[0]} dataset="{dset.name}" '
                                      f'file=""')

            elif 'o' in self._frame_mode or 'O' in self._frame_mode:
                shape_diff = 0

            elif 'x' in self._frame_mode:
                logger.info(f'msg="Resetting dataset" index={index} file={fname} '
                            f'frames={dset.shape[0]} dataset="{dset.name}"')
                dset.resize((0, *(dset.shape[1:])))

                shape_diff = index+1

            else:
                raise RuntimeError(f'BUG: No shape diff for mode: {self._frame_mode}')

        if shape_diff > 0:
            logger.debug(f'msg="Resizing dataset" file="{dset.file.filename}" '
                         f'name={dset.name} size={dset.shape[0]} '
                         f'index={index} diff={shape_diff} idiff={idiff}')
            dset.resize((dset.shape[0]+shape_diff, *(dset.shape[1:])))


    def push_data(self, index, **data):
        '''
        Received for every data point in a scan.

        Args:
            index: Integer to determine the position of the current
              data point in the overall (larger) dataset. This should
              always point to the next available index in the first
              dimention, i.e. if the existing dataset has dimension
              (37, N, M), with the current data point to become
              the 38th, then `index` needs to be 37 (counting starts
              at 0).

              Behavior if the index doesn't match the shape is defined
              by the class-global parameter `mode`.

              If this is `None`, the next free slot (i.e. current_size+1)
              is used, essentially making the operation always succeed
              as if "append" mode were active.
              
            **data: dictionary from data name ("tag") to data arrays
        '''

        with self._h5obj(init=False) as h5:

            self._ensure_group(h5, self._h5group)

            if self._h5group not in ('', '/'):
                h5node = h5[self._h5group]
            else:
                h5node = h5
            
            for key, container in data.items():
                self._ensure_dataset(grpobj=h5node,
                                     name=key,
                                     dtype=container.dtype,
                                     point_shape=container.shape)
                dset = h5node[key]

                if index is None:
                    index = dset.shape[0]
                
                self._ensure_frame(dset, index)
                
                item = np.array(container)
                dset[index] = item



class Processor(SinkBase):
    '''
    Saves data as a dataset in a HDF5 file.

    The HDF5 file / dataset is opened explicitly for each dataset,
    on each run through the pipeline. Files that don't exist are
    created (though not filesystem folders), and files that do
    are appended to (`h5py` mode "a").

    The sink tries to make it easy to obtain uniform, synchronous,
    well-defined arrays of data of the same length. It does so
    mostly by filling up empty frame slots when there isn't any
    data available, or by overwriting data if necessary, according
    to the user specification. This is governed according to the
    `mode` initialization parameter, which determines what to
    do when a dataset already exists.
    '''
    
    def __init__(self,
                 path: str,
                 mode: str = 'a+',
                 index: str = '',
                 strict: bool = True,
                 timeout: float = 0.0,
                 ):
        '''
        Args:
            path: the path format. Generally, the expected syntax is
              "<HDF5-file>#<path-within-file>". The part beyond "#"
              represents the path to the dataset within the HDF5 file.
              The path within file may be just a simple dataset, or may
              contain HDF5 group elements ("#/path/to/group/dataset").
              All groups that don't exist are created.
        
              Note that this is a *format* which will be used for each
              incoming data set, so it should contain at least some
              differentiating element for substitution. Available elements
              are:
                - all the context keys
                - `index` for the designated numeric index of the
                  pipeline run (see `index`)
                - `tag` for the name / tag of the dataset being processed
              
              If the path within HDF5 ends in "/", or is an empty string,
              then it is assumed to be a group, and the format suffix `"{tag}"`
              is automatically assumed.

            mode:  Must be one of `a` (append), `o` (overwrite) or
              `x` (reset), possibly in combination with `+` (top-up):
        
                 - `a`: require that the data point be always appended
                   to the current dataset -- never overwrite or delete
                   existing data.
        
                 - `o`: overwrite already existing data points (frames).

                 - `O`: same as `o`, but additioally delete and re-create
                   whole dataset entries, if the shape or data type of the
                   existing dataset does not match the new request.

                 - `x`: reset the entire dataset (i.e. delete all existing
                   data points) if a data point already exists at the
                   specified index.

                 - `+`: top-up marker will fill up empty slots, but without
                    actually writing any data to them. They will remain
                    filled with default HDF5 settings according  to the data
                    type. If top-up is not specified, otherwise the operation
                    will fail if index is higher than the one of the next
                    slot in turn.
        
            index: name of the context variable which contains the current
              frame index (preferrably integer). If this is an empty string,
              no index is used and essentially every operation is an "append".

            strict: if this is `True` (the default), then any saving errors
              being raised will be allowed to bubble up to the pipe processor.
              Typically, this means the application is being shut down.
              When `False`, then `RefuseIndex` type of errors (typically when
              a frame index is out of place) are being reported, but ignored.

            timeout: If the target HDF5 file is locked, how long to wait for
              unlocking. Default is 5 seconds. Set to 0 to disable waiting,
              in which case a locked file will result in failing to save.
        '''
        super().__init__()
        
        parts = path.split('#')
        
        if len(parts) == 1:
            self.h5file = parts[0]
            self.h5grp = '/{tag}'
        elif len(parts) == 2:
            self.h5file, self.h5grp = parts
        else:
            raise RuntimeError(f'msg="Bad HDF5 path, expected <file>[#<group>[/<dataset>]]" '
                               f'path="path"')

        if (len(self.h5grp)==0) or \
           (self.h5grp[-1]=='/') or \
           self._has_group(self.h5file, self.h5grp):
            self.h5grp += (('/' if self.h5grp[-1] != '/' else '') + '{tag}')

        
        logger.info(f'msg="Initializing HDF5 saver" file="{self.h5file}" group="{self.h5grp}"')

        self._index_ctx_tag = index

        self._stacker_mode = mode

        self._current_file_and_node = (None, None)

        self._strict = strict

        self._unlock_timeout = timeout


    def _has_group(self, fpath, grp):
        try:
            with h5py.File(fpath, 'r') as h5:
                if isinstance(h5[grp], h5py.Group):
                    return True
        except KeyError:
            pass
        except OSError:
            pass

        return False


    def ensure_folder_of(self, path):
        d = os.path.dirname(path)
        if (len(d) > 0):
            if not os.path.exists(d):
                os.makedirs(d)
                return
            if (not os.path.isdir(d)):
                raise RuntimeError(f'msg="Path is required to be a folder folder" '
                                   f'path="{p}"')    


    def get_index(self, context):
        if self._index_ctx_tag not in (None, ''):
            try:
                if self._index_ctx_tag[0] == '@':
                    _index = context[self._index_ctx_tag[1:]]
                else:
                    _index = context[self._index_ctx_tag]
            except KeyError as e:
                avail = ','.join(context.keys())
                err = \
                    f'msg="Index key not available in this frame" ' \
                    f'expected="{self._index_ctx_tag}" ' \
                    f'available="{avail}"'
                raise RefuseIndex(err)
        else:
            _index = None

        return _index    
        

    def handle_index_error(self, err, tag=None):
        if self._strict or not isinstance(err, RefuseIndex):
            raise err
        logger.error(err)
        logger.error(f'msg="Ignoring frame index error as instructed" tag={tag}')


    async def _store_dataset(self, tag, contents, h5path, h5group, h5dset, index):
        ## Attempts to store data.
        ## Returns the full path of the dataset / index, if successful.
        t0 = time.time()
        while True:
            try:
                stor = Hdf5DataStacker(h5file=h5path, h5group=h5group,
                                       mode=self._stacker_mode)
                stor.push_data(index=index, **{h5dset: contents})
                return f'{h5path}#{h5group}/{h5dset}[{index}]'
            except BlockingIOError as e:
                if time.time()-t0 >= self._unlock_timeout:
                    await asyncio.sleep(1e-5 * random.random())
                    continue
                raise


    def _make_h5_target(self, tag, context):
        ## Generates the final target saving path
        
        h5path = self.h5file.format(tag=tag, **context)
        tmp = self.h5grp.format(tag=tag, **context).split('/')

        h5group = '/'.join(tmp[:-1])
        h5dtset = tmp[-1]

        self.ensure_folder_of(h5path)

        return h5path, h5group, h5dtset
        

    async def __call__(self, data=None, context=None):
        
        if data is None:
            data = {}
        if context is None:
            context = {}

        try:
            _index = self.get_index(context)
        except RefuseIndex as e:
            self.handle_index_error(e)
            logger.warning(f'msg="Skipping frame altogether"')
            return
        
        result = {}
        for tag, cont in data.items():
            h5path, h5grp, h5dset = self._make_h5_target(tag, context)
            try:
                result[tag] = await self._store_dataset(tag, cont, h5path,
                                                        h5grp, h5dset, _index)
            except RefuseIndex as e:
                self.handle_index_error(e)

        return result
