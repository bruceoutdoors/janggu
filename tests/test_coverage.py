import os

import matplotlib
matplotlib.use('AGG')  # pylint: disable=

import numpy as np
import pandas
import pkg_resources
import pytest

from janggu.data import Cover



def test_bam_inferred_binsize():
    data_path = pkg_resources.resource_filename('janggu', 'resources/')
    bed_file = os.path.join(data_path, "positive.bed")

    bamfile_ = os.path.join(data_path, "sample.bam")

    cover = Cover.create_from_bam(
        'test',
        bamfiles=bamfile_,
        regions=bed_file,
        flank=0,
        storage='ndarray')
    assert len(cover) == 25
    assert cover.shape == (25, 200, 2, 1)

def test_bigwig_inferred_binsize():
    data_path = pkg_resources.resource_filename('janggu', 'resources/')
    bed_file = os.path.join(data_path, "positive.bed")

    bwfile_ = os.path.join(data_path, "sample.bw")

    cover = Cover.create_from_bigwig(
        'test',
        bigwigfiles=bwfile_,
        resolution=1,
        regions=bed_file,
        storage='ndarray')
    assert len(cover) == 25
    assert cover.shape == (25, 200, 1, 1)

def test_bed_inferred_binsize():
    data_path = pkg_resources.resource_filename('janggu', 'resources/')
    bed_file = os.path.join(data_path, "positive.bed")

    #file_ = os.path.join(data_path, "sample.bw")

    cover = Cover.create_from_bed(
        'test',
        bedfiles=bed_file,
        regions=bed_file,
        resolution=1,
        storage='ndarray')
    assert len(cover) == 25
    assert cover.shape == (25, 200, 1, 1)

def test_cover_from_bam_sanity():
    data_path = pkg_resources.resource_filename('janggu', 'resources/')
    bed_file = os.path.join(data_path, "sample.bed")

    bamfile_ = os.path.join(data_path, "sample.bam")
    cover = Cover.create_from_bam(
        'test',
        bamfiles=bamfile_,
        regions=bed_file,
        binsize=200, stepsize=200,
        flank=0,
        storage='ndarray')
    cover[0]

    cov2 = Cover.create_from_bam(
           'test',
           bamfiles=bamfile_,
           storage='ndarray')
    assert len(cover.gindexer) == len(cover.garray.handle)
    assert len(cov2.garray.handle) != len(cover.garray.handle)

    with pytest.raises(Exception):
        # name must be a string
        Cover.create_from_bam(
            1.2,
            bamfiles=bamfile_,
            regions=bed_file,
            binsize=1, stepsize=1,
            storage='ndarray')

    with pytest.raises(Exception):
        Cover.create_from_bam(
            'test',
            bamfiles=bamfile_,
            regions=bed_file,
            binsize=1, stepsize=1,
            flank=-1,
            storage='ndarray')
    with pytest.raises(Exception):
        Cover.create_from_bam(
            'test',
            bamfiles=bamfile_,
            regions=bed_file,
            binsize=1, stepsize=-1,
            flank=0,
            storage='ndarray')
    with pytest.raises(Exception):
        Cover.create_from_bam(
            'test',
            bamfiles=bamfile_,
            regions=bed_file,
            binsize=-1, stepsize=1,
            flank=0,
            storage='ndarray')


def test_cover_from_bigwig_sanity():
    data_path = pkg_resources.resource_filename('janggu', 'resources/')
    bed_file = os.path.join(data_path, "sample.bed")

    bwfile_ = os.path.join(data_path, "sample.bw")
    cover = Cover.create_from_bigwig(
        'test',
        bigwigfiles=bwfile_,
        regions=bed_file,
        binsize=200, stepsize=50,
        resolution=50,
        flank=0,
        storage='ndarray')
    cover[0]
    cov2 = Cover.create_from_bigwig(
        'test',
        bigwigfiles=bwfile_,
        resolution=50,
        storage='ndarray')
    assert len(cover.gindexer) == len(cover.garray.handle)
    assert len(cov2.garray.handle) != len(cover.garray.handle)

    with pytest.raises(Exception):
        # name must be a string
        Cover.create_from_bigwig(
            1.2,
            bigwigfiles=bwfile_,
            regions=bed_file,
            binsize=1, stepsize=1,
            storage='ndarray')

    with pytest.raises(Exception):
        Cover.create_from_bigwig(
            'test',
            bigwigfiles=bwfile_,
            regions=bed_file,
            binsize=1, stepsize=1,
            flank=-1,
            storage='ndarray')
    with pytest.raises(Exception):
        Cover.create_from_bigwig(
            'test',
            bigwigfiles=bwfile_,
            regions=bed_file,
            binsize=1, stepsize=-1,
            flank=0,
            storage='ndarray')
    with pytest.raises(Exception):
        Cover.create_from_bigwig(
            'test',
            bigwigfiles=bwfile_,
            regions=bed_file,
            binsize=-1, stepsize=1,
            flank=0,
            storage='ndarray')
    with pytest.raises(Exception):
        # resolution must be greater than stepsize
        Cover.create_from_bigwig(
            'test',
            bigwigfiles=bwfile_,
            regions=bed_file,
            binsize=200, stepsize=50,
            resolution=300,
            flank=0,
            storage='ndarray')


def test_cover_from_bed_sanity():
    data_path = pkg_resources.resource_filename('janggu', 'resources/')
    bed_file = os.path.join(data_path, 'sample.bed')

    bwfile_ = os.path.join(data_path, "scored_sample.bed")
    cover = Cover.create_from_bed(
        'test',
        bedfiles=bwfile_,
        regions=bed_file,
        binsize=200, stepsize=50,
        resolution=50,
        flank=0,
        storage='ndarray')
    cover[0]
    Cover.create_from_bed(
        'test',
        bedfiles=bwfile_,
        regions=bed_file,
        binsize=200, stepsize=50,
        resolution=50,
        storage='ndarray')

    with pytest.raises(Exception):
        # name must be a string
        Cover.create_from_bed(
            1.2,
            bedfiles=bwfile_,
            regions=bed_file,
            binsize=1, stepsize=1,
            storage='ndarray')

    with pytest.raises(Exception):
        Cover.create_from_bed(
            'test',
            bedfiles=bwfile_,
            regions=bed_file,
            binsize=1, stepsize=1,
            flank=-1,
            storage='ndarray')
    with pytest.raises(Exception):
        Cover.create_from_bed(
            'test',
            bedfiles=bwfile_,
            regions=bed_file,
            binsize=1, stepsize=-1,
            flank=0,
            storage='ndarray')
    with pytest.raises(Exception):
        Cover.create_from_bed(
            'test',
            bedfiles=bwfile_,
            regions=bed_file,
            binsize=-1, stepsize=1,
            flank=0,
            storage='ndarray')
    with pytest.raises(Exception):
        # resolution must be greater than stepsize
        Cover.create_from_bed(
            'test',
            bedfiles=bwfile_,
            regions=bed_file,
            binsize=200, stepsize=50,
            resolution=300,
            flank=0,
            storage='ndarray')
    with pytest.raises(Exception):
        csvfile = os.path.join(data_path, 'ctcf_sample.csv')
        # must be a bed file
        Cover.create_from_bed(
            'test',
            bedfiles=csvfile,
            regions=bed_file,
            binsize=1, stepsize=1,
            storage='ndarray')


def test_cover_bam_unstranded():
    data_path = pkg_resources.resource_filename('janggu', 'resources/')
    bamfile_ = os.path.join(data_path, "sample.bam")
    gsfile_ = os.path.join(data_path, 'sample.chrom.sizes')

    content = pandas.read_csv(gsfile_, sep='\t', names=['chr', 'length'],
                              index_col='chr')

    gsize = content.to_dict()['length']

    bed_file = os.path.join(data_path, "sample.bed")


    cover = Cover.create_from_bam(
        "yeast_I_II_III.bam",
        bamfiles=bamfile_,
        regions=bed_file,
        binsize=200, stepsize=200,
        genomesize=gsize,
        stranded=False)

    np.testing.assert_equal(len(cover), 100)
    np.testing.assert_equal(cover.shape, (100, 200, 1, 1))

    # the region is read relative to the forward strand
    # read on the reverse strand
    val = np.where(cover[4] == 1)
    np.testing.assert_equal(cover[4].sum(), 1.)
    np.testing.assert_equal(val[1][0], 179)  # pos

    # two reads on the forward strand
    val = np.where(cover[13] == 1)
    np.testing.assert_equal(cover[13].sum(), 2.)
    np.testing.assert_equal(val[1], np.asarray([162, 178]))  # pos

    # the region is read relative to the reverse strand
    # for index 50
    # read on the reverse strand
    val = np.where(cover[52] == 1)
    np.testing.assert_equal(cover[52].sum(), 2.)
    np.testing.assert_equal(val[1], np.asarray([9, 89]))  # pos

    # two reads on the forward strand
    val = np.where(cover[96] == 1)
    np.testing.assert_equal(cover[96].sum(), 1.)
    np.testing.assert_equal(val[1], np.asarray([25]))  # pos


def test_cover_bam_paired_5pend():
    # sample2.bam contains paired end examples,
    # unmapped examples, unmapped mate and low quality example
    data_path = pkg_resources.resource_filename('janggu', 'resources/')
    bamfile_ = os.path.join(data_path, "sample2.bam")

    cover = Cover.create_from_bam(
        "yeast_I_II_III.bam",
        bamfiles=bamfile_,
        stranded=False,
        pairedend='5pend',
        min_mapq=30)

    assert cover.garray.handle['ref'].sum() == 2, cover.garray.handle['ref']

    # the read starts at index 6 and tlen is 39
    assert cover.garray.handle['ref'][6, 0, 0] == 1
    # another read maps to index 24
    assert cover.garray.handle['ref'][24, 0, 0] == 1


def test_cover_bam_paired_midpoint():
    # sample2.bam contains paired end examples,
    # unmapped examples, unmapped mate and low quality example
    data_path = pkg_resources.resource_filename('janggu', 'resources/')
    bamfile_ = os.path.join(data_path, "sample2.bam")


    cover = Cover.create_from_bam(
        "yeast_I_II_III.bam",
        bamfiles=bamfile_,
        stranded=False,
        pairedend='midpoint',
        min_mapq=30)

    assert cover.garray.handle['ref'].sum() == 2, cover.garray.handle['ref']
    print(cover.garray.handle['ref'])
    # the read starts at index 6 and tlen is 39
    assert cover.garray.handle['ref'][6 + 39//2, 0, 0] == 1
    # another read maps to index 34
    assert cover.garray.handle['ref'][34, 0, 0] == 1


def test_cover_bam(tmpdir):
    os.environ['JANGGU_OUTPUT'] = tmpdir.strpath
    data_path = pkg_resources.resource_filename('janggu', 'resources/')
    bamfile_ = os.path.join(data_path, "sample.bam")
    gsfile_ = os.path.join(data_path, 'sample.chrom.sizes')

    content = pandas.read_csv(gsfile_, sep='\t', names=['chr', 'length'],
                              index_col='chr')

    gsize = content.to_dict()['length']

    bed_file = os.path.join(data_path, "sample.bed")

    for store in ['ndarray', 'hdf5', 'sparse']:
        # base pair binsize
        # print(store)
        cover = Cover.create_from_bam(
            "yeast_I_II_III.bam",
            bamfiles=bamfile_,
            regions=bed_file,
            binsize=200, stepsize=200,
            genomesize=gsize,
            storage=store, cache=True)

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 200, 2, 1))

        # the region is read relative to the forward strand
        # read on the reverse strand
        val = np.where(cover[4] == 1)
        np.testing.assert_equal(cover[4].sum(), 1.)
        np.testing.assert_equal(val[1][0], 179)  # pos
        np.testing.assert_equal(val[2][0], 1)  # strand

        # two reads on the forward strand
        val = np.where(cover[13] == 1)
        np.testing.assert_equal(cover[13].sum(), 2.)
        np.testing.assert_equal(val[1], np.asarray([162, 178]))  # pos
        np.testing.assert_equal(val[2], np.asarray([0, 0]))  # strand

        # the region is read relative to the reverse strand
        # for index 50
        # read on the reverse strand
        val = np.where(cover[52] == 1)
        np.testing.assert_equal(cover[52].sum(), 2.)
        np.testing.assert_equal(val[1], np.asarray([9, 89]))  # pos
        np.testing.assert_equal(val[2], np.asarray([0, 0]))  # strand

        # two reads on the forward strand
        val = np.where(cover[96] == 1)
        np.testing.assert_equal(cover[96].sum(), 1.)
        np.testing.assert_equal(val[1], np.asarray([25]))  # pos
        np.testing.assert_equal(val[2], np.asarray([1]))  # strand


def test_load_bam_resolution10(tmpdir):
    os.environ['JANGGU_OUTPUT'] = tmpdir.strpath
    data_path = pkg_resources.resource_filename('janggu', 'resources/')
    bamfile_ = os.path.join(data_path, "sample.bam")
    gsfile_ = os.path.join(data_path, 'sample.chrom.sizes')

    content = pandas.read_csv(gsfile_, sep='\t', names=['chr', 'length'],
                              index_col='chr')

    gsize = content.to_dict()['length']

    bed_file = os.path.join(data_path, "sample.bed")

    for store in ['ndarray', 'hdf5', 'sparse']:
        # base pair binsize
        # print(store)
        cover = Cover.create_from_bam(
            "yeast_I_II_III.bam",
            bamfiles=bamfile_,
            regions=bed_file,
            binsize=200, stepsize=200,
            genomesize=gsize,
            resolution=10,
            storage=store, cache=True)

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 20, 2, 1))

        # the region is read relative to the forward strand
        # read on the reverse strand
        val = np.where(cover[4] == 1)
        np.testing.assert_equal(cover[4].sum(), 1.)
        np.testing.assert_equal(val[1][0], 17)  # pos
        np.testing.assert_equal(val[2][0], 1)  # strand

        # two reads on the forward strand
        val = np.where(cover[13] == 1)
        np.testing.assert_equal(cover[13].sum(), 2.)
        np.testing.assert_equal(val[1], np.asarray([16, 17]))  # pos
        np.testing.assert_equal(val[2], np.asarray([0, 0]))  # strand

        # the region is read relative to the reverse strand
        # for index 50
        # read on the reverse strand
        val = np.where(cover[52] == 1)
        np.testing.assert_equal(cover[52].sum(), 2.)
        np.testing.assert_equal(val[1], np.asarray([0, 8]))  # pos
        np.testing.assert_equal(val[2], np.asarray([0, 0]))  # strand

        # two reads on the forward strand
        val = np.where(cover[96] == 1)
        np.testing.assert_equal(cover[96].sum(), 1.)
        np.testing.assert_equal(val[1], np.asarray([2]))  # pos
        np.testing.assert_equal(val[2], np.asarray([1]))  # strand


def test_load_cover_bigwig_default(tmpdir):
    os.environ['JANGGU_OUTPUT'] = tmpdir.strpath
    data_path = pkg_resources.resource_filename('janggu', 'resources/')

    bwfile_ = os.path.join(data_path, "sample.bw")
    gsfile_ = os.path.join(data_path, 'sample.chrom.sizes')

    gsize = pandas.read_csv(gsfile_, sep='\t', names=['chr', 'length'],
                            index_col='chr').to_dict()['length']

    bed_file = os.path.join(data_path, "sample.bed")

    for store in ['ndarray', 'hdf5', 'sparse']:
        # base pair binsize
        print(store)
        cover = Cover.create_from_bigwig(
            "cov",
            bigwigfiles=bwfile_,
            regions=bed_file,
            binsize=200, stepsize=200,
            genomesize=gsize,
            storage=store, cache=True)

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 1, 1, 1))

        # there is one read in the region
        np.testing.assert_allclose(cover[4].sum(), 36./200)
        np.testing.assert_allclose(cover[52].sum(), 2*36./200)


def test_load_cover_bigwig_resolution1(tmpdir):
    os.environ['JANGGU_OUTPUT'] = tmpdir.strpath
    data_path = pkg_resources.resource_filename('janggu', 'resources/')

    bwfile_ = os.path.join(data_path, "sample.bw")

    bed_file = os.path.join(data_path, "sample.bed")

    for store in ['ndarray', 'hdf5', 'sparse']:
        # base pair binsize
        print(store)
        cover = Cover.create_from_bigwig(
            "cov",
            bigwigfiles=bwfile_,
            regions=bed_file,
            binsize=200, stepsize=200,
            resolution=1,
            storage=store, cache=True)

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 200, 1, 1))

        # there is one read in the region 4
        np.testing.assert_allclose(cover[4].sum(), 36)
        np.testing.assert_equal(cover[4][0, :, 0, 0],
         np.asarray(
          [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
           1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
           1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0.,
           0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))
        # and two reads in region 52
        np.testing.assert_allclose(cover[52].sum(), 2*36)
        np.testing.assert_equal(cover[52][0, :, 0, 0],
        np.asarray(
        [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1.,
         1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
         1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
         1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
         1., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
         0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))


def test_load_cover_bed_binary(tmpdir):
    os.environ['JANGGU_OUTPUT'] = tmpdir.strpath
    bed_file = pkg_resources.resource_filename('janggu', 'resources/sample.bed')
    score_file = pkg_resources.resource_filename('janggu',
                                                 'resources/scored_sample.bed')

    for store in ['ndarray', 'hdf5', 'sparse']:
        print('store', store)
        cover = Cover.create_from_bed(
            "cov",
            bedfiles=score_file,
            regions=bed_file,
            binsize=200, stepsize=200,
            resolution=200,
            storage=store,
            mode='binary', cache=True)

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 1, 1, 1))
        np.testing.assert_equal(cover[0].sum(), 0)
        np.testing.assert_equal(cover[4].sum(), 1)

        cover = Cover.create_from_bed(
            "cov50",
            bedfiles=score_file,
            regions=bed_file,
            binsize=200, stepsize=200,
            storage=store,
            resolution=50,
            mode='binary', cache=True)

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 4, 1, 1))
        np.testing.assert_equal(cover[0].sum(), 0)
        np.testing.assert_equal(cover[4].sum(), 4*1)

        cover = Cover.create_from_bed(
            "cov50",
            bedfiles=score_file,
            regions=bed_file,
            binsize=200, stepsize=200,
            storage=store,
            #resolution=50,
            dimmode='first',
            mode='binary', cache=True)

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 1, 1, 1))
        np.testing.assert_equal(cover[0].sum(), 0)
        np.testing.assert_equal(cover[4].sum(), 1)


def test_load_cover_bed_scored():
    bed_file = pkg_resources.resource_filename('janggu', 'resources/sample.bed')
    score_file = pkg_resources.resource_filename('janggu',
                                                 'resources/scored_sample.bed')

    for store in ['ndarray', 'sparse']:
        cover = Cover.create_from_bed(
            "cov",
            bedfiles=score_file,
            regions=bed_file,
            binsize=200, stepsize=200,
            resolution=200,
            storage=store,
            mode='score')

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 1, 1, 1))
        np.testing.assert_equal(cover[0].sum(), 0)
        np.testing.assert_equal(cover[4].sum(), 5)

        cover = Cover.create_from_bed(
            "cov50",
            bedfiles=score_file,
            regions=bed_file,
            binsize=200, stepsize=200,
            storage=store,
            resolution=50,
            mode='score')

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 4, 1, 1))
        np.testing.assert_equal(cover[0].sum(), 0)
        np.testing.assert_equal(cover[4].sum(), 4*5)

        cover = Cover.create_from_bed(
            "cov50",
            bedfiles=score_file,
            regions=bed_file,
            storage=store,
            binsize=200, stepsize=200,

            dimmode='first',
            mode='score')

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 1, 1, 1))
        np.testing.assert_equal(cover[0].sum(), 0)
        np.testing.assert_equal(cover[4].sum(), 5)


def test_load_cover_bed_categorical():
    bed_file = pkg_resources.resource_filename('janggu', 'resources/sample.bed')
    score_file = pkg_resources.resource_filename('janggu',
                                                 'resources/scored_sample.bed')

    for store in ['ndarray', 'sparse']:
        cover = Cover.create_from_bed(
            "cov",
            bedfiles=score_file,
            regions=bed_file,
            binsize=200, stepsize=200,
            resolution=200,
            storage=store,
            mode='categorical')

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 1, 1, 6))
        np.testing.assert_equal(cover[0].sum(), 0)
        np.testing.assert_equal(cover[4].sum(), 1)

        cover = Cover.create_from_bed(
            "cov50",
            bedfiles=score_file,
            regions=bed_file,
            binsize=200, stepsize=200,
            resolution=50,
            storage=store,
            mode='categorical')

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 4, 1, 6))
        np.testing.assert_equal(cover[0].sum(), 0)
        np.testing.assert_equal(cover[4].sum(), 4*1)

        cover = Cover.create_from_bed(
            "cov50",
            bedfiles=score_file,
            regions=bed_file,
#            resolution=50,
            binsize=200, stepsize=200,
            storage=store,
            dimmode='first',
            mode='categorical')

        np.testing.assert_equal(len(cover), 100)
        np.testing.assert_equal(cover.shape, (100, 1, 1, 6))
        np.testing.assert_equal(cover[0].sum(), 0)
        np.testing.assert_equal(cover[4].sum(), 1)
